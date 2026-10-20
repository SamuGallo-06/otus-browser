from PySide6.QtWidgets import (
    QLineEdit, QMainWindow, QSizePolicy, QWidget
)
from PySide6.QtCore import QUrl, QUrlQuery
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtGui import QIcon

from ui.ui_mainwindow import Ui_MainWindow
from ui import resources_rc

from settings import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
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
        
        #Tabs
        self.browserTabWidget.tabCloseRequested.connect(self.close_tab)
        self.browserTabWidget.currentChanged.connect(self.on_tab_changed)
        
        self.browserTabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) #This makes the browser view large as bog as the main window
        
        self.new_tab(HOME_URL)
    
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
        """Indirizzo se sembra un indirizzo, altrimenti ricerca."""
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
    
    def new_tab(self, url: str = "https://example.com") -> QWebEngineView:
        view = QWebEngineView()
        view.load(QUrl(url))
        index = self.browserTabWidget.addTab(view, "Nuova scheda")
        self.browserTabWidget.setCurrentIndex(index)

        view.titleChanged.connect(
            lambda title, v=view: self.browserTabWidget.setTabText(self.browserTabWidget.indexOf(v), title[:25])
        )
        view.urlChanged.connect(
            lambda qurl, v=view: self.on_url_changed(v, qurl)
        )
        return view

    def current_view(self) -> QWebEngineView | None:
        widget = self.browserTabWidget.currentWidget()
        if isinstance(widget, QWebEngineView):
            return widget
        return None

    def on_url_changed(self, view, qurl):
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
    