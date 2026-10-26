import subprocess
import platform
import os

from PySide6.QtWidgets import QBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

from custom.download_view_item import DownloadViewItem
from downloads import Download, DownloadManager
from utils import open_file

from ui.ui_download_manager import Ui_DownloadHistory

class DownloadHistoryView(QWidget):
    pauseRequested = Signal(Download)
    resumeRequested = Signal(Download)
    cancelRequested = Signal(Download)
     
    def __init__(self, parent=None, download_manager: DownloadManager | None = None):
        super().__init__(parent)
        self.ui = Ui_DownloadHistory()
        self.setWindowFlag(Qt.WindowType.Window)
        self.ui.setupUi(self)
        if download_manager is None:
            return
        else:
            self.download_manager = download_manager
        self.download_list = self.download_manager.load() if download_manager else []
        print(f"DownloadHistoryView initialized with {len(self.download_list)} downloads.")
        layout = self.ui.scrollAreaWidgetContents.layout()
        if not isinstance(layout, QBoxLayout):
            raise RuntimeError("scrollAreaWidgetContents must have a box layout")
        self.downloads_layout: QBoxLayout = layout
        
        self.ui.clearHistoryButton.clicked.connect(self.clear_history)
        self.ui.searchBox.textChanged.connect(self.onSearchTextChanged)
        self.refresh_view()
    
    def refresh_view(self):
        self.download_list = self.download_manager.get_download_history()
        
        self.clear_layout()
        
        if self.downloads_layout is None:
            print("Error: downloads_layout is None. Cannot add download items.")
            return
                 
        placeholder = self.downloads_layout.takeAt(0)
        if placeholder is not None:
            if placeholder.widget() is not None:
                placeholder.widget().deleteLater() #type: ignore
        
        for download in self.download_list:
            print(f"Adding download to history view: {download.filename}, status: {download.status}")
            element = DownloadViewItem(download)
            element.deleteRequested.connect(self.remove_download)
            element.pauseRequested.connect(self.pauseRequested.emit)
            element.resumeRequested.connect(self.resumeRequested.emit)
            element.cancelRequested.connect(self.cancelRequested.emit)
            self.download_manager.downloadUpdated.connect(element.update_download)
            self.downloads_layout.addWidget(element)
            
        self.downloads_layout.addStretch()
        self.apply_filter(self.ui.searchBox.text())  # keep the current filter
            
    def clear_layout(self):
        if(self.downloads_layout is None):
            print("Error: No layout found to clear.")
            return
        while self.downloads_layout.count():
            item = self.downloads_layout.takeAt(0)          # detach the item from the layout
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)       # hide it immediately
                widget.deleteLater()         # free it when control returns to the event loop
               
    def remove_download(self, download: Download):
        print(f"Removing download from history view: {download.filename}")
        self.download_manager.remove(download, self.refresh_view)
        
    def clear_history(self):
        print("Clearing download history.")
        self.download_manager.clear_history(self.refresh_view)
        
    def onSearchTextChanged(self, text: str):
        self.apply_filter(text)

    def apply_filter(self, text: str):
        if self.downloads_layout is None:
            return
        query = text.strip().casefold()

        for i in range(self.downloads_layout.count()):
            item = self.downloads_layout.itemAt(i)
            widget = item.widget() if item is not None else None
            # Skip stretch/spacer items and anything that isn't a download row
            if not isinstance(widget, DownloadViewItem):
                continue

            d = widget.download
            match = query in d.filename.casefold() or query in d.source.casefold()
            widget.setVisible(match)
            
    