from PySide6.QtWidgets import (
    QFileDialog, QLineEdit, QMainWindow, QSizePolicy, QWidget, QMessageBox
)
from PySide6.QtCore import QUrl, QUrlQuery, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineDownloadRequest
from PySide6.QtGui import QIcon, Qt

from pathlib import Path
import logging

from bookmarks import Bookmark, BookmarkManager
from ui.ui_mainwindow import Ui_MainWindow
from ui.ui_download import Ui_DownloadWidget
from ui import resources_rc
from views.download_widget import DownloadWidget
from views.webview import OtusWebView


from settings import *
from utils import *
from profiles import OtusProfile

logger = logging.getLogger(__name__)

SAVE_FORMATS = {
    "Web page, single file (*.html)":   QWebEngineDownloadRequest.SavePageFormat.SingleHtmlSaveFormat,
    "Web page, complete (*.html)":      QWebEngineDownloadRequest.SavePageFormat.CompleteHtmlSaveFormat,
    "MHTML archive (*.mhtml)":          QWebEngineDownloadRequest.SavePageFormat.MimeHtmlSaveFormat,
}

class BrowserPage(QWebEnginePage):
    def __init__(self, profile, create_tab, parent=None):
        super().__init__(profile, parent)
        self.create_tab = create_tab

    def createWindow(self, _window_type):
        view = self.create_tab()
        return view.page()

class MainWindow(QMainWindow, Ui_MainWindow):
    
    exitRequested = Signal()
    closed = Signal(object)
    
    def __init__(self, profile: OtusProfile | None = None,
                 profile_id: str = "OtusProfile"):
        super().__init__()
        if profile is None:
            profile = OtusProfile(uid=profile_id, name=profile_id)
        self.profile_data = profile
        
        logger.debug("Initializing MainWindow with profile: %s", self.profile_data.uid)
        self.setupUi(self)
        self.setupActions()
        
        # Set the size policy of the browser tab widget to expand and fill the available space
        self.browserTabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) #This makes the browser view large as bog as the main window
        logger.debug("Setting up profile: %s", self.profile_data.uid)
        self.setup_profile(self.profile_data)
        
        # Setting Profile's Library
        self.bookmarks = BookmarkManager(self.profile_data, persistent=self.profile_data.type != "Nocturnal" and self.profile_data.type != "Guest")
        self.downloads = []  # List to keep track of active download widgets. It will be replaced with a more robust download manager in the future.
        
        self.bookmarks.reloadRequired.connect(self.__rebuild_bookmarks_menu)
        self.__rebuild_bookmarks_menu()
        
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
        # File
        self.actionNew_Tab.triggered.connect(lambda: self.new_tab(HOME_URL))
        self.actionNew_Window.triggered.connect(self.newWindow)
        self.actionNew_Private_Window.triggered.connect(self.newNocturnalWindow)
        self.actionClose_Tab.triggered.connect(lambda: self.close_tab(self.browserTabWidget.currentIndex()))
        self.actionOpen_File.triggered.connect(self.openFile)
        self.actionSave_Page.triggered.connect(self.savePage)
        self.actionExit.triggered.connect(self.requestExit)
        
        # Edit
        self.actionCopy.triggered.connect(self.browserCopy)
        self.actionCut.triggered.connect(self.browserCut)
        self.actionPaste.triggered.connect(self.browserPaste)
        self.actionSelect_All.triggered.connect(self.browserSelectAll)
        
        # View
        self.actionZoom_in.triggered.connect(self.browserZoomIn)
        self.actionZoom_out.triggered.connect(self.browserZoomOut)
        self.actionReset_Zoom.triggered.connect(self.browserResetZoom)
        self.actionToggle_Fullscreen.triggered.connect(self.toggleFullscreen)
        
        # Bookmarks
        self.actionAdd_Bookmark.triggered.connect(self.add_bookmark)
        self.actionBookmark_all_tabs.triggered.connect(self.bookmark_all_tabs)
        
        # Help
        self.actionAbout_Otus.triggered.connect(self.show_about_dialog)
        
        # Tabs
        self.browserTabWidget.tabCloseRequested.connect(self.close_tab)
        self.browserTabWidget.currentChanged.connect(self.on_tab_changed)
        
    def setup_profile(self, profile: OtusProfile):
        # Profile
        # Create a persistent profile for the browser to store cookies, cache, and other data
        # Profile data is stored under .local/share/OtusBrowser/Profiles using the profile UID.
        # This allows the browser to maintain state across sessions.
        self.profile = QWebEngineProfile(profile.uid, self)
        profile_path = profile.storage_path
        profile_path.mkdir(parents=True, exist_ok=True)
        self.profile.setPersistentStoragePath(str(profile_path))
        
        self.profile.downloadRequested.connect(self.onDownloadRequested)
        self.profile.setDownloadPath(str(get_download_path()))

    def get_current_profile(self) -> OtusProfile:
        """Return the data structure for the profile currently used by this window."""
        return self.profile_data
    
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
    
    def new_tab(self, url: str | None = None) -> OtusWebView:
        view = OtusWebView()
        view.linkNewTabRequested.connect(self.openLinkInNewTab)
        view.linkNewWindowRequested.connect(self.openLinkInNewWindow)
        view.searchRequested.connect(self.searchSelection)
        view.savePageRequested.connect(self.savePage)
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
    
    def searchSelection(self, text: str):
        query = QUrlQuery()
        query.addQueryItem("q", text)
        url = QUrl(SEARCH_URL)
        url.setQuery(query)
        self.openLinkInNewTab(url)

    def current_view(self) -> OtusWebView | None:
        widget = self.browserTabWidget.currentWidget()
        if isinstance(widget, OtusWebView):
            return widget
        return None

    def on_url_changed(self, view, qurl):
        logger.debug("URL changed in tab: %s", qurl.toString())
        if view is self.current_view():
            self.urlBar.setText(qurl.toString())

    def close_tab(self, index: int):
        #LClosing the last tab means the user want to exit the browser
        if self.browserTabWidget.count() <= 1:
            self.requestExit()
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

    def on_load_started(self, view: OtusWebView):
        logger.debug("Started loading page: %s", view.url().toString())
        self.statusbar.showMessage("Loading page {pageUrl}".format(pageUrl=view.url()))
        
    def on_load_progress(self, view: OtusWebView, progress):
        self.statusbar.showMessage("Loading({progress}%)...".format(progress=progress))

    def on_load_finished(self, view: OtusWebView, ok):
        if ok:
            logger.debug("Page loaded successfully: %s", view.url().toString())
            self.statusbar.showMessage("Loaded \"{pageName}\"".format(pageName=view.title()), 5000)       
        else:
            logger.error("Failed to load page: %s", view.url().toString())
            self.statusbar.showMessage("Failed to load page {pageUrl}".format(pageUrl=view.url().toString()))   
               
    # Web page navigation events
    
    def openLinkInNewTab(self, url: QUrl):
        self.new_tab(url.toString())
      
    def openLinkInNewWindow(self, url: QUrl):
        window = MainWindow(profile=self.profile_data)
        current_view = window.current_view()
        if current_view is not None:
            current_view.setUrl(url)
            
        window.show()
     
    # File Downloads

    def onDownloadRequested(self, request: QWebEngineDownloadRequest):
        if request.isSavePageDownload():
            # path and filename are already set by the browser, no need to ask the user
            widget = DownloadWidget(request, parent=self)
            self.downloads.append(widget)
            widget.show()
            request.accept()
            return
        
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
            
    ######################################
    ##     File Menu                    ##
    ######################################
    
    def openFile(self):
        logger.debug("Open file action triggered")

        filePath = QFileDialog.getOpenFileName(
            self,
            "Open File",
            str(Path.home()),
            f"Supported files ({', '.join(SUPPORTED_OPEN_FILE_EXTENSIONS)});;All files (*)"
        )[0]
        
        path = f"file://{filePath.replace(" ","%20")}"
        url = self.text_to_url(path)
        
        if not filePath:
            return
        
        if not Path(filePath).suffix.lower() in SUPPORTED_OPEN_FILE_EXTENSIONS:
            QMessageBox.warning(
                self,
                "Unsupported file type",
                f"The selected file type is not supported for viewing in the browser.\n\n"
                f"Supported file types: {', '.join(SUPPORTED_OPEN_FILE_EXTENSIONS)}",
                QMessageBox.StandardButton.Ok
            )
            return
        
        self.openLinkInNewTab(url)
        
    def savePage(self):
        logger.debug("Save page action triggered")
        view = self.current_view()
        if view is None:
            return
        title = sanitize_filename(view.title() or "page")
        start = str(Path(get_download_path()) / f"{title}.html")

        path, selected_filter = QFileDialog.getSaveFileName(
            self, "Save page as", start, ";;".join(SAVE_FORMATS)
        )
        if not path:
            return
        view.page().save(path, SAVE_FORMATS[selected_filter])

    def newWindow(self):
        logger.debug("New window action triggered")
        new_window = MainWindow(profile_id="OtusProfile")
        new_window.show()
        
    def newNocturnalWindow(self):
        logger.debug("New nocturnal window action triggered")
        new_window = MainWindow(profile_id="OtusNocturnal")
        new_window.show()
        
    def requestExit(self):
        logger.info("Exiting application requested by user.")
        self.exitRequested.emit()

    def closeEvent(self, event):
        event.accept()
        self.closed.emit(self.profile_data)
        
    ######################################
    ##     Edit Menu                    ##
    ######################################
    
    def browserCut(self):
        view = self.current_view()
        if view is not None:
            view.triggerPageAction(QWebEnginePage.WebAction.Cut) 
            
    def browserCopy(self):
            view = self.current_view()
            if view is not None:
                view.triggerPageAction(QWebEnginePage.WebAction.Copy)
                
    def browserPaste(self):
            view = self.current_view()
            if view is not None:
                view.triggerPageAction(QWebEnginePage.WebAction.Paste)
                
    def browserSelectAll(self):
        view = self.current_view()
        if view is not None:
            view.triggerPageAction(QWebEnginePage.WebAction.SelectAll)
            
    ######################################
    ##     View Menu                    ##
    ######################################  
    
    def browserZoomIn(self):
        view = self.current_view()
        if view is not None:
            current_zoom = view.zoomFactor()
            view.setZoomFactor(current_zoom + 0.1)
    
    def browserZoomOut(self):
        view = self.current_view()
        if view is not None:
            current_zoom = view.zoomFactor()
            view.setZoomFactor(current_zoom - 0.1)
            
    def browserResetZoom(self):
        view = self.current_view()
        if view is not None:
            view.setZoomFactor(1.0)
            
    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
            
    ######################################
    ##    Bookmarks Menu                ##
    ######################################
    
    def add_bookmark(self):
        view = self.current_view()
        if view is not None:
            url = view.url().toString()
            title = view.title()
            bookmark = Bookmark(url=url, title=title, desc="")
            self.bookmarks.add_bookmark(bookmark)
            
    def bookmark_all_tabs(self):
        for i in range(self.browserTabWidget.count()):
            view = self.browserTabWidget.widget(i)
            if isinstance(view, OtusWebView):
                url = view.url().toString()
                title = view.title()
                bookmark = Bookmark(url=url, title=title, desc="")
                self.bookmarks.add_bookmark(bookmark)
            
    def __rebuild_bookmarks_menu(self):
        defaults = [self.actionAdd_Bookmark, self.actionBookmark_all_tabs, self.actionManage_bookmarks, self.actionShow_bookmarks_bar]
        
        self.menuBookmarks.clear()
        for d in defaults:
            self.menuBookmarks.addAction(d)
            
        self.menuBookmarks.addSeparator()
        
        bookmarks = self.bookmarks.load_bookmarks()
        for bookmark in bookmarks:
            action = self.menuBookmarks.addAction(bookmark.title)
            action.setToolTip(bookmark.url)
            action.triggered.connect(lambda checked, url=bookmark.url: self.openLinkInNewTab(QUrl(url)))
        
            
    ######################################
    ##     Help Menu                    ##
    ######################################
    
    def show_about_dialog(self):
        QMessageBox.about(
            self,
            "About Otus Browser",
            "<h2>Otus Browser</h2>"
            "<p>Version 1.0</p>"
            "<p>A privacy-focused web browser built with PySide6 and Qt WebEngine.</p>"
            "<p>For more information, visit <a href='https://github.com/SamuGallo-06/otus-browser'>the project repository</a>.</p>"
        )