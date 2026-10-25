from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from custom.download_view_item import DownloadViewItem
from downloads import Download

from ui.ui_download_manager import Ui_DownloadHistory

class DownloadHistoryView(QWidget):
     
    def __init__(self, parent=None, download_list: list[Download] | None = None):
        super().__init__(parent)
        self.ui = Ui_DownloadHistory()
        self.setWindowFlag(Qt.WindowType.Window)
        self.ui.setupUi(self)
        self.download_list = download_list or []
        print(f"DownloadHistoryView initialized with {len(self.download_list)} downloads.")
        self.downloads_layout = self.ui.scrollAreaWidgetContents.layout()

        self.refresh_view()
    
    def refresh_view(self):
        
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
            self.downloads_layout.addWidget(element)
            
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
        #Handle the removal of the download from the list and update the view, using the download manger to remove it from the history
        self.refresh_view()    
        
            
    