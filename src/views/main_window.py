import json

from PySide6.QtWidgets import (
    QApplication, QFileDialog, QLabel, QLineEdit, QListWidgetItem, QMainWindow, QMenu, QSizePolicy, QTreeView, QVBoxLayout, QWidget, QMessageBox
)
from PySide6.QtCore import QSortFilterProxyModel, QUrl, QUrlQuery, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineDownloadRequest
from PySide6.QtGui import QIcon, Qt

from pathlib import Path
import logging

from bookmarks import Bookmark
from downloads import Download
from ui.ui_mainwindow import Ui_MainWindow
from ui import resources_rc
from user_settings import (
    ProfileSettings,
    SettingsManager,
    get_app_settings,
)
from views.about_dialog import AboutDialog
from views.bookmarks_library import BookmarksLibraryView
from views.download_history import DownloadHistoryView
from views.history_view import HistoryView
from views.settings_window import SettingsWindow
from views.webview import OtusWebView
from views.download_widget import DownloadWidget


from settings import *
from utils import *
from profiles import OtusProfile
from profile_context import ProfileContext

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
    
    def __init__(
        self,
        profile: OtusProfile | None = None,
        profile_id: str = "OtusProfile",
        profile_settings: SettingsManager[ProfileSettings] | None = None,
        start_url: str | None = None
    ):
        super().__init__()
        self._child_windows: list[MainWindow] = []
        if profile is None:
            profile = OtusProfile(uid=profile_id, name=profile_id)
        self.profile_data = profile
        if profile_settings is None:
            raise ValueError("profile_settings is required")
        self.profile_settings = profile_settings
        
        logger.debug("Initializing MainWindow with profile: %s", self.profile_data.uid)
        self.setupUi(self)
        self.setupActions()
        
        # Set the size policy of the browser tab widget to expand and fill the available space
        self.browserTabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) #This makes the browser view large as bog as the main window
        logger.debug("Setting up profile: %s", self.profile_data.uid)
        # The web profile, ad blocker and library managers are shared by all the windows
        # that use the same profile, so they are owned by the ProfileContext, not by the window.
        self.context = ProfileContext.for_profile(
            self.profile_data, self.profile_settings
        )
        self.profile = self.context.profile
        self.adblock_policy = self.context.adblock_policy
        self.silent_wing_policy = self.context.silent_wing_policy
        self.context.silentWingChanged.connect(self._sync_silent_wing_action)
        self.context.blockedCountChanged.connect(self._update_tracker_count)
        self.profile_settings.settingsChanged.connect(self._update_tracker_visibility)
        self.tracker_count_label = QLabel(self)
        self.statusbar.addPermanentWidget(self.tracker_count_label)
        self._sync_silent_wing_action(self.silent_wing_policy.enabled)
        self._update_tracker_count(self.context.total_blocked_count)
        self._update_tracker_visibility()
        self.bookmarks = self.context.bookmarks
        self.downloads = self.context.downloads
        self.history = self.context.history
        
        self.bookmarks.reloadRequired.connect(self.__rebuild_bookmarks_menu)
        self.__rebuild_bookmarks_menu()
        
        self.start_url = start_url
        self.create_session()
        
    def setupActions(self):
        # Address Bar
        self.urlBar = QLineEdit()
        self.urlBar.setPlaceholderText(self.tr("Search or enter address"))
        self.urlBar.setClearButtonEnabled(True)
        self.urlBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.toolBar.insertWidget(self.actionSilentwing, self.urlBar)
        self.urlBar.returnPressed.connect(self.navigate)

        # Toolbar Actions
        self.actionBack.triggered.connect(self.navigate_back)
        self.actionForward.triggered.connect(self.navigate_forward)
        self.actionReload.triggered.connect(self.navigate_reload)
        self.actionHome.triggered.connect(self.navigate_home)
        self.actionSilentwing.toggled.connect(self.set_silent_wing)

        # Menu Actions
        # File
        self.actionNew_Tab.triggered.connect(
            lambda: self.new_tab(self.profile_settings.settings.home_url)
        )
        self.actionNew_Window.triggered.connect(self.newWindow)
        self.actionNew_Private_Window.triggered.connect(self.newNocturnalWindow)
        self.actionClose_Tab.triggered.connect(lambda: self.close_tab(self.browserTabWidget.currentIndex()))
        self.actionOpen_File.triggered.connect(self.openFile)
        self.actionSave_Page.triggered.connect(self.savePage)
        self.actionExit.triggered.connect(self.close)
        
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
        
        # Tools
        self.actionDownloads.triggered.connect(self.on_download_history)
        self.actionManage_bookmarks.triggered.connect(self.on_bookmarks_library)
        self.actionHistory.triggered.connect(self.on_history)
        self.actionPreferences.triggered.connect(self.open_settings_window)
        
        # Help
        self.actionAbout_Otus.triggered.connect(self.show_about_dialog)
        
        # Tabs
        self.browserTabWidget.tabCloseRequested.connect(self.close_tab)
        self.browserTabWidget.currentChanged.connect(self.on_tab_changed)
        
    def create_session(self):
        if self.start_url is not None:
            self.new_tab(self.start_url)
        
        if self.profile_settings.settings.restore_previous_session:
            try:
                with open(self.profile_data.storage_path / "previous_session.json", "r") as f:
                    session_data = json.load(f)
                    open_tabs = session_data.get("open_tabs", [])
                    for url in open_tabs:
                        if isinstance(url, str) and url.strip():
                            self.new_tab(url)

                    self.actionSilentwing.setChecked(
                        session_data.get("silent_wing_enabled", False)
                    )
                    if not open_tabs:
                        self.new_tab()
            except FileNotFoundError:
                logger.info("No previous session found to restore.")
                self.new_tab(self.profile_settings.settings.home_url)
            except Exception as e:
                logger.error("Failed to restore previous session: {err}".format(err=e))
                QMessageBox.critical(
                    self,
                    self.tr("Error"),
                    self.tr(
                        "Failed to restore previous session. A new session will be started."
                    ),
                    QMessageBox.StandardButton.Ok
                )
        elif self.profile_settings.settings.use_startup_pages:
            pages = self.profile_settings.settings.startup_pages
            if pages:
                for page in pages:
                    self.new_tab(page)
            else:
                self.new_tab(self.profile_settings.settings.home_url)
        else:
            self.new_tab(self.profile_settings.settings.home_url)

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

    def set_silent_wing(self, enabled: bool) -> None:
        """Toggle SilentWing for the shared profile and reload the current tab."""
        self.context.set_silent_wing_enabled(enabled)
        logger.info(
            "SilentWing %s", "enabled" if enabled else "disabled"
        )
        self.statusBar().showMessage(
            self.tr("SilentWing {state}").format(
                state=self.tr("on") if enabled else self.tr("off")
            ),
            5000,
        )
        if view := self.current_view():
            view.reload()

    def _sync_silent_wing_action(self, enabled: bool) -> None:
        self.actionSilentwing.blockSignals(True)
        self.actionSilentwing.setChecked(enabled)
        self.actionSilentwing.blockSignals(False)
        self.actionSilentwing.setToolTip(
            self.tr("Silent Wing ({state}) - {count} blocked").format(
                state=self.tr("on") if enabled else self.tr("off"),
                count=self.context.total_blocked_count,
            )
        )

    def _update_tracker_count(self, count: int) -> None:
        self.tracker_count_label.setText(
            self.tr("Blocked trackers: {count}").format(count=count)
        )
        self._sync_silent_wing_action(self.silent_wing_policy.enabled)

    def _update_tracker_visibility(self) -> None:
        self.tracker_count_label.setVisible(
            self.profile_settings.settings.show_tracker_count
        )
        
    def navigate(self, url: str | None = None):
        if url is not None:
            target = QUrl(url)
        else:
            #if no url is provided, use the text in the address bar
            text = self.urlBar.text().strip()
            target = text_to_url(text, self.profile_settings.settings.search_url)
        
        view = self.current_view()
        if view and target.isValid():
            view.load(target)
            
    def navigate_home(self):
        view = self.current_view()
        if view:
            view.load(QUrl(self.profile_settings.settings.home_url))
    
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
        view.renderProcessTerminated.connect(
            lambda status, exit_code, v=view: self.on_render_process_terminated(
                v, status, exit_code
            )
        )
        if url:
            view.load(QUrl(url))
            
        logger.debug(
            "New tab created with URL: {url}".format(
                url=(url if url else "None")
            )
        )
        
        return view
    
    def searchSelection(self, text: str):
        query = QUrlQuery()
        query.addQueryItem("q", text)
        url = QUrl(self.profile_settings.settings.search_url)
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
            logger.debug(
                "Tab changed to index %d with URL: %s",
                index,
                view.url().toString(),
            )

    def on_load_started(self, view: OtusWebView):
        logger.debug("Started loading page: %s", view.url().toString())
        self.statusbar.showMessage(
            self.tr("Loading page {pageUrl}").format(pageUrl=view.url())
        )
        
    def on_load_progress(self, view: OtusWebView, progress):
        self.statusbar.showMessage(
            self.tr("Loading({progress}%)...").format(progress=progress)
        )

    def on_load_finished(self, view: OtusWebView, ok):
        url = view.url().toString()
        title = view.title()
        self.setWindowTitle(
            self.tr("{title} - Otus Browser").format(title=title or url)
        )
        if ok and view.url().scheme() in ("http", "https"):
            self.history.add_visit(url, title or url)
            logger.debug("Page loaded successfully: {pageUrl}".format(pageUrl=url))
            self.statusbar.showMessage(
                self.tr('Loaded "{pageName}"').format(pageName=title), 5000
            )
        else:
            logger.error("Failed to load page: {pageUrl}".format(pageUrl=url))
            self.statusbar.showMessage(
                self.tr("Failed to load page {pageUrl}").format(pageUrl=url)
            )
            
        self.check_bookmark()  

    def on_render_process_terminated(self, view, status, exit_code):
        logger.error(
            "WebEngine render process terminated for %s: status=%s, exit_code=%s",
            view.url().toString(),
            status,
            exit_code,
        )
        self.statusbar.showMessage(
            self.tr(
                "Il processo di rendering della pagina è terminato. Ricarica la pagina."
            )
        )
               
    # Web page navigation events
    
    def openLinkInNewTab(self, url: QUrl):
        self.new_tab(url.toString())
      
    def openLinkInNewWindow(self, url: QUrl):
        window = MainWindow(
            profile=self.profile_data,
            profile_settings=self.profile_settings,
        )
        self._child_windows.append(window)
        current_view = window.current_view()
        if current_view is not None:
            current_view.setUrl(url)
        window.destroyed.connect(
            lambda _object=None, child=window: self._child_windows.remove(child)
            if child in self._child_windows else None
        )
        window.show()
     
    # File Downloads

    def onDownloadRequested(self, request: QWebEngineDownloadRequest):
        if request.isSavePageDownload():
            # path and filename are already set by the browser, no need to ask the user
            record = self.downloads.accept(request)
            widget = DownloadWidget(record, self.downloads, parent=self)
            widget.show()
            return
        
        dw_name = sanitize_filename(request.suggestedFileName())
        dw_host = request.url().host() or "(unknown host)"
        logger.debug("Download requested")

        self.statusbar.showMessage(
            self.tr("Download requested: {filename}").format(filename=dw_name),
            5000,
        )

        # Downloa Requested
        if Path(dw_name).suffix.lower() in RISKY_DOWNLOAD_EXTENSIONS:
            box = QMessageBox(
                QMessageBox.Icon.Warning,
                self.tr("Suspicious Download"),
                self.tr(
                    "File «{dw_name}» is a potentially risky file. "
                    "(such as an executable or script)\n"
                    "Source: {dw_host}\n\n"
                    "Downloading and executing files from the internet can be dangerous. "
                    "Do you want to download it anyway?"
                ).format(dw_name=dw_name, dw_host=dw_host),
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
        if self.profile_settings.settings.ask_for_download_path:
            suggested = str(get_download_path(self.profile_settings) / name)
            path, _ = QFileDialog.getSaveFileName(
                self, self.tr("Save download as"), suggested, self.tr("All files (*)"),
            )
            if not path:
                self.cancelDownload(request)  # user dismissed the dialog
                return
            target = Path(path)
            request.setDownloadDirectory(str(target.parent))
            request.setDownloadFileName(target.name)
        else:
            directory = str(get_download_path(self.profile_settings))
            request.setDownloadDirectory(directory)
            request.setDownloadFileName(unique_path(directory, name))
        
        record = self.downloads.accept(request)
        widget = DownloadWidget(record, self.downloads, parent=self)
        widget.show()
        logger.debug("Download accepted")

    def cancelDownload(self, request: QWebEngineDownloadRequest):
        request.cancel()
        
        logger.debug("Download canceled")

    def pause_download(self, download: Download):
        self.downloads.pause(download)

    def resume_download(self, download: Download):
        self.downloads.resume(download)

    def cancel_download(self, download: Download):
        self.downloads.cancel(download)

            
    ######################################
    ##     File Menu                    ##
    ######################################
    
    def openFile(self):
        logger.debug("Open file action triggered")

        filePath = QFileDialog.getOpenFileName(
            self,
            self.tr("Open File"),
            str(Path.home()),
            self.tr("Supported files ({extensions});;All files (*)").format(
                extensions=", ".join(SUPPORTED_OPEN_FILE_EXTENSIONS)
            ),
        )[0]
        
        path = f"file://{filePath.replace(" ","%20")}"
        url = text_to_url(path, self.profile_settings.settings.search_url)
        
        if not filePath:
            return
        
        if not Path(filePath).suffix.lower() in SUPPORTED_OPEN_FILE_EXTENSIONS:
            QMessageBox.warning(
                self,
                self.tr("Unsupported file type"),
                self.tr(
                    "The selected file type is not supported for viewing in the browser.\n\n"
                    "Supported file types: {extensions}"
                ).format(extensions=", ".join(SUPPORTED_OPEN_FILE_EXTENSIONS)),
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
        start = str(
            get_download_path(self.profile_settings) / f"{title}.html"
        )

        path, selected_filter = QFileDialog.getSaveFileName(
            self,
            self.tr("Save page as"),
            start,
            ";;".join(SAVE_FORMATS),
        )
        if not path:
            return
        view.page().save(path, SAVE_FORMATS[selected_filter])

    def newWindow(self):
        logger.debug("New window action triggered")
        new_window = MainWindow(
            profile=self.profile_data,
            profile_settings=self.profile_settings,
        )
        self._child_windows.append(new_window)
        new_window.destroyed.connect(
            lambda _object=None, child=new_window: self._child_windows.remove(child)
            if child in self._child_windows else None
        )
        new_window.show()
        
    def newNocturnalWindow(self):
        logger.debug("New nocturnal window action triggered")
        nocturnal_profile = OtusProfile(uid="OtusNocturnal", name="OtusNocturnal")
        nocturnal_settings = SettingsManager(
            nocturnal_profile.storage_path / "settings.ini",
            ProfileSettings,
            parent=self,
        )
        new_window = MainWindow(
            profile=nocturnal_profile,
            profile_settings=nocturnal_settings,
        )
        self._child_windows.append(new_window)
        new_window.destroyed.connect(
            lambda _object=None, child=new_window: self._child_windows.remove(child)
            if child in self._child_windows else None
        )
        new_window.show()
        
    def _is_last_window_of_profile(self) -> bool:
        """True if no other visible window is using the same profile as this one."""
        return not any(
            isinstance(w, MainWindow) and w is not self and w.isVisible()
            and w.profile_data.uid == self.profile_data.uid
            for w in QApplication.topLevelWidgets()
        )

    def closeEvent(self, event):
        if get_app_settings().settings.always_ask_before_exit:
            box = QMessageBox(
                QMessageBox.Icon.Question,
                self.tr("Exit Confirmation"),
                self.tr("Are you sure you want to exit the browser?"),
                parent=self,
            )
            box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            box.setDefaultButton(QMessageBox.StandardButton.Cancel)
        
            if box.exec() == QMessageBox.StandardButton.Cancel:
                event.ignore()  # keeps the window open
                return
            
        if self.profile_settings.settings.restore_previous_session:
            previousSession = {}
            open_tabs = []
            for index in range(self.browserTabWidget.count()):
                widget = self.browserTabWidget.widget(index)

                if not isinstance(widget, OtusWebView):
                    continue

                open_tabs.append(widget.url().toString())
                
            previousSession["open_tabs"] = open_tabs
            previousSession["silent_wing_enabled"] = self.actionSilentwing.isChecked()
            try: 
                with open(self.profile_data.storage_path / "previous_session.json", "w") as f:
                    json.dump(previousSession, f, indent=4)
            except Exception as e:
                logger.error("Failed to save previous session: %s", e)
                QMessageBox.critical(
                    self,
                    self.tr("Error"),
                    self.tr(
                        "Failed to save previous session. Changes will not be saved."
                    ),
                    QMessageBox.StandardButton.Ok
                )
            
        # Downloads are shared by every window of the profile: only ask when closing the last one
        if self._is_last_window_of_profile() and self.downloads.active_downloads():
            answer = QMessageBox.question(
                self,
                self.tr("Downloads in progress"),
                self.tr("Some downloads are still running. Quit and cancel them?"),
            )
            if answer != QMessageBox.StandardButton.Yes:
                event.ignore()  # keeps the window open
                return
            self.downloads.cancel_all()
        self.closed.emit(self.profile_data)
        event.accept()
        
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
            self.actionToggle_Fullscreen.setText(self.tr("Enter Fullscreen"))
            self.actionToggle_Fullscreen.setIcon(QIcon(FEATHER_ICON_PACK + "maximize.svg"))
        else:
            self.showFullScreen()
            self.actionToggle_Fullscreen.setText(self.tr("Exit Fullscreen"))
            self.actionToggle_Fullscreen.setIcon(QIcon(FEATHER_ICON_PACK + "minimize.svg"))

    ######################################
    ##    Bookmarks Menu                ##
    ######################################
    
    def add_bookmark(self):
        view = self.current_view()
        if view is not None:
            url = view.url().toString()
            title = view.title()
            bookmark = Bookmark(url=url, title=title, desc="")
            self.bookmarks.save_icon(bookmark.url, view.icon())
            self.bookmarks.add_bookmark(bookmark)
            
        self.check_bookmark()
            
    def bookmark_all_tabs(self):
        for i in range(self.browserTabWidget.count()):
            view = self.browserTabWidget.widget(i)
            if isinstance(view, OtusWebView):
                url = view.url().toString()
                title = view.title()
                bookmark = Bookmark(url=url, title=title, desc="")
                self.bookmarks.add_bookmark(bookmark)
                
    def remove_bookmark(self):
        view = self.current_view()
        if view is not None:
            url = view.url().toString()
            b = self.bookmarks.search(url)
            if b is not None:
                self.bookmarks.deleteBookmark(b)
                
            self.check_bookmark()
                
    def check_bookmark(self):
        view = self.current_view()
        if view is not None:
            url = view.url().toString()
            if(self.bookmarks.has_bookmark(url)):
                self.actionAdd_Bookmark.setText(self.tr("Remove Bookmark"))
                self.actionAdd_Bookmark.triggered.connect(self.remove_bookmark)
            else:
                self.actionAdd_Bookmark.setText(self.tr("Add Bookmark"))
                self.actionAdd_Bookmark.triggered.connect(self.add_bookmark) 
            
    def __rebuild_bookmarks_menu(self):
        defaults = [self.actionAdd_Bookmark, self.actionBookmark_all_tabs, self.actionManage_bookmarks]
        
        self.menuBookmarks.clear()
        for d in defaults:
            self.menuBookmarks.addAction(d)
            
        self.menuBookmarks.addSeparator()
        
        bookmarks = self.bookmarks.load_bookmarks()
        for bookmark in bookmarks:
            action = self.menuBookmarks.addAction(bookmark.title)
            action.setToolTip(bookmark.url)
            action.triggered.connect(lambda checked, url=bookmark.url: self.openLinkInNewTab(QUrl(url)))
            
    #######################################
    ##     Tools Menu                    ##
    #######################################
    
    def on_download_history(self):
        self.download_history_view = DownloadHistoryView(parent=self, download_manager=self.downloads)
        self.download_history_view.pauseRequested.connect(self.pause_download)
        self.download_history_view.resumeRequested.connect(self.resume_download)
        self.download_history_view.cancelRequested.connect(self.cancel_download)
        self.download_history_view.show()

    def on_bookmarks_library(self):
        self.bookmarks_library = BookmarksLibraryView(parent=self, bookmarks=self.bookmarks.bookmarks)
        self.bookmarks_library.delete_requested.connect(self.on_bookmark_delete_requested)
        self.bookmarks.reloadRequired.connect(self.bookmarks_library.refresh_view)
        self.bookmarks_library.elementSaved.connect(self.on_bookmark_saved)
        self.bookmarks_library.show()
        
    def on_bookmark_delete_requested(self, bookmark: Bookmark):
        print(f"Bookmark delete requested for {bookmark}")
        self.bookmarks.deleteBookmark(bookmark)

    def on_bookmark_saved(self):
        print("Bookmark saved.")
        self.bookmarks.save_bookmarks()
        
    def on_history(self):
        self.history_view = HistoryView(parent=self, history_manager=self.history)
        self.history_view.openUrlRequested.connect(lambda url: self.openLinkInNewTab(QUrl(url)))
        self.history_view.show()
        
    def open_settings_window(self):
        self.settings_window = SettingsWindow(
            profile_settings=self.profile_settings,
            parent=self,
        )
        self.settings_window.show()

    ######################################
    ##     Help Menu                    ##
    ######################################
    
    def show_about_dialog(self):
        aboutDialog = AboutDialog(parent=self)
        aboutDialog.exec()