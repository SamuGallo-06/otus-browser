from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

class OtusWebView(QWebEngineView):
    linkNewTabRequested = Signal(QUrl)
    searchRequested = Signal(str)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        data = self.lastContextMenuRequest()
        act = menu.addAction("Open Link in a New Tab")
        #act.triggered.connect(self.copyCleanLink)
        menu.popup(event.globalPos())