from PySide6.QtWidgets import (
    QLineEdit, QMainWindow, QSizePolicy, QWidget, QMessageBox
)
from PySide6.QtCore import QUrl, QUrlQuery
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineDownloadRequest
from PySide6.QtGui import QIcon, Qt

from pathlib import Path
import logging

from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_download import Ui_DownloadWidget
from ui import resources_rc

from settings import *
from utils import *
from views.download_widget import DownloadWidget

logger = logging.getLogger(__name__)

class BrowserPage(QWebEnginePage):
    def __init__(self, profile, create_tab, parent=None):
        super().__init__(profile, parent)
        self.create_tab = create_tab

    def createWindow(self, _window_type):
        view = self.create_tab()
        return view.page()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, profile_name: str = "OtusProfile"):
        super().__init__()
        logger.debug("Initializing MainWindow with profile: %s", profile_name)
        self.setupUi(self)
        
        self.setupActions()
        
        self.browserTabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) #This makes the browser view large as bog as the main window
        
        logger.debug("Setting up profile: %s", profile_name)
        self.setup_profile(profile_name)
        
        self.downloads = []  # List to keep track of active download widgets
        
        self.new_tab(HOME_URL)
        
    def setupActions(self):
        # Address Bar
        self.urlBar = QLineEdit()
        self.urlBar.setPlaceholderText("Search or enter address")
        self.urlBar.setClearButtonEnabled(True)
        self.urlBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.toolBar.insertWidget(self.actionSilentwing, self.urlBar)
        self.urlBar.returnPressed.connect(self.navigate)

        # Toolbar Actions
        self.actionBack.triggered.connect(self.navigate_back)
        self.actionForward.triggered.connect(self.navigate_forward)
        self.actionReload.triggered.connect(self.navigate_reload)
        self.actionHome.triggered.connect(self.navigate_home)
        self.actionSilentwing.setIcon(QIcon(":/App Icons/otus_shield.svg"))

        # Menu Actions
        self.actionNew_Tab.triggered.connect(lambda: self.new_tab(HOME_URL))

        # Tabs
        self.browserTabWidget.tabCloseRequested.connect(self.close_tab)
        self.browserTabWidget.currentChanged.connect(self.on_tab_changed)
                
        
    def setup_profile(self, profile_name):
        # Profile
        # Create a persistent profile for the browser to store cookies, cache, and other data
        # Profile data will be stored in the user's home directory under .local/share/OtusBrowser/Profiles/OtusProfile for the default profile, named "OtusProfile". 
        # This allows the browser to maintain state across sessions.
        self.profile = QWebEngineProfile(profile_name, self)
        profile_path = PROFILES_DIR / profile_name
        profile_path.mkdir(parents=True, exist_ok=True)
        self.profile.setPersistentStoragePath(str(profile_path))
        
        self.profile.downloadRequested.connect(self.onDownloadRequested)
        self.profile.setDownloadPath(str(get_download_path()))
    
    def navigate_back(self):
        if view := self.current_view():
            view.back()

    def navigate_forward(self):
        if view := self.current_view():
            view.forward()

    def navigate_reload(self):
        if view := self.current_view():
            view.reload()
        
    def navigate(self):
        text = self.urlBar.text().strip()
        view = self.current_view()
        if text and view:
            view.load(self.text_to_url(text))

    def navigate_home(self):
        view = self.current_view()
        if view:
            view.load(QUrl(HOME_URL))

    def text_to_url(self, text: str) -> QUrl:
        """Address bar input can be a URL or a search query. This function determines which it is and returns the appropriate QUrl."""
        looks_like_address = " " not in text and (
            "://" in text or "." in text or text.startswith("localhost")
        )
        if looks_like_address:
            url = QUrl.fromUserInput(text)
            if url.isValid():
                # fromUserInput usa http se manca lo schema: per un browser
                # privacy meglio https (localhost escluso)
                if "://" not in text and url.scheme() == "http" and url.host() != "localhost":
                    url.setScheme("https")
                return url

        query = QUrlQuery()
        query.addQueryItem("q", text)
        url = QUrl(SEARCH_URL)
        url.setQuery(query)
        return url
    
    # Tabs
    
    def new_tab(self, url: str | None = None) -> QWebEngineView:
        view = QWebEngineView()
        page = BrowserPage(self.profile, self.new_tab, view)
        view.setPage(page)
        index = self.browserTabWidget.addTab(view, "New Tab")
        self.browserTabWidget.setCurrentIndex(index)

        view.titleChanged.connect(
            lambda title, v=view: self.browserTabWidget.setTabText(self.browserTabWidget.indexOf(v), title[:25])
        )
        view.urlChanged.connect(
            lambda qurl, v=view: self.on_url_changed(v, qurl)
        )
        view.loadStarted.connect(
            lambda v=view: self.on_load_started(v)
        )
        view.loadProgress.connect(
            lambda progress, v=view: self.on_load_progress(v, progress)
        )
        view.loadFinished.connect(
            lambda ok, v=view: self.on_load_finished(v, ok)
        )
        if url:
            view.load(QUrl(url))
        
        logger.debug("New tab created with URL: %s", url if url else "None")
        return view

    def current_view(self) -> QWebEngineView | None:
        widget = self.browserTabWidget.currentWidget()
        if isinstance(widget, QWebEngineView):
            return widget
        return None

    def on_url_changed(self, view, qurl):
        logger.debug("URL changed in tab: %s", qurl.toString())
        if view is self.current_view():
            self.urlBar.setText(qurl.toString())

    def close_tab(self, index: int):
        #LClosing the last tab means the user want to exit the browser
        if self.browserTabWidget.count() <= 1:
            self.close()
            return  
                      
        widget = self.browserTabWidget.widget(index)
        self.browserTabWidget.removeTab(index)
        if widget is not None:
            widget.deleteLater()
        
    def on_tab_changed(self, index: int):
        view = self.current_view()
        if view:
            self.urlBar.setText(view.url().toString())
            logger.debug("Tab changed to index %d with URL: %s", index, view.url().toString())

    def on_load_started(self, view: QWebEngineView):
        logger.info("Started loading page: %s", view.url().toString())
        self.statusbar.showMessage("Loading page {pageUrl}".format(pageUrl=view.url()))
        
    def on_load_progress(self, view: QWebEngineView, progress):
        self.statusbar.showMessage("Loading({progress}%)...".format(progress=progress))

    def on_load_finished(self, view: QWebEngineView, ok):
        if ok:
            logger.info("Page loaded successfully: %s", view.url().toString())
            self.statusbar.showMessage("Loaded \"{pageName}\"".format(pageName=view.title()), 5000)       
        else:
            logger.error("Failed to load page: %s", view.url().toString())
            self.statusbar.showMessage("Failed to load page {pageUrl}".format(pageName=view.url()))   
          
            
            
    # Web page navigation events
    
    def openLinkInNewTab(self, url: QUrl):
        self.new_tab(url.toString())
        
    # File Downloads

    def onDownloadRequested(self, request: QWebEngineDownloadRequest):
        dw_name = sanitize_filename(request.suggestedFileName())
        dw_host = request.url().host() or "(unknown host)"
        logger.debug("Download requested")

        self.statusbar.showMessage(f"Download requested: {dw_name}", 5000)

        # Downloa Requested
        if Path(dw_name).suffix.lower() in RISKY_DOWNLOAD_EXTENSIONS:
            box = QMessageBox(
                QMessageBox.Icon.Warning,
                "Suspicious Download",
                "File «{dw_name}» is a potentially risky file. (such as an executable or script)\n"
                "Source: {dw_host}\n\n"
                "Downloading and executing files from the internet can be dangerous. "
                "Do you want to download it anyway?".format(dw_name=dw_name, dw_host=dw_host),
                parent=self,
            )
            box.setTextFormat(Qt.TextFormat.PlainText)
            box.setDetailedText(request.url().toString())
            box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            box.setDefaultButton(QMessageBox.StandardButton.Cancel)

            if box.exec() == QMessageBox.StandardButton.Yes:
                self.acceptDownload(request, dw_name)
            else:
                self.cancelDownload(request)
        else:
            self.acceptDownload(request, dw_name)

    def acceptDownload(self, request: QWebEngineDownloadRequest, name: str):
        directory = str(get_download_path())
        request.setDownloadDirectory(directory)
        request.setDownloadFileName(unique_path(directory, name))

        widget = DownloadWidget(request, parent=self)
        self.downloads.append(widget)
        widget.show()

        request.accept()
        logger.debug("Download accepted")

    def cancelDownload(self, request: QWebEngineDownloadRequest):
        request.cancel()
        logger.debug("Download canceled")
        
    def updateProgress(self, request):
        received = request.receivedBytes()
        totals = request.totalBytes()      # -1 if download size is unknown
        if totals > 0:
            perc = int(received * 100 / totals)
            self.statusbar.showMessage(f"Download: {perc}%")
        else:
            self.statusbar.showMessage(f"Download: {received // 1024} KB")