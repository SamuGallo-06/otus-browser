from PySide6.QtWidgets import QBoxLayout, QSizePolicy, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

from bookmarks import Bookmark
from custom.bookmark_view_item import BookmarkViewItem

from utils import open_file

from ui.ui_bookmarks import Ui_BookmarksLibrary
from ui.ui_edit_bookmark import Ui_EditBookmarkDialog
from views.edit_bookmark_dialog import EditBookmarkDialog

class BookmarksLibraryView(QWidget):
    
    delete_requested = Signal(Bookmark)
    elementSaved = Signal()
     
    def __init__(self, parent=None, bookmarks: list[Bookmark] = []):
        super().__init__(parent)
        self.bookmarks = bookmarks
        self.setWindowFlag(Qt.WindowType.Window)
        self.ui = Ui_BookmarksLibrary()
        self.ui.setupUi(self)
        
        l = self.ui.scrollAreaWidgetContents.layout()
        if not isinstance(l, QBoxLayout):
            raise RuntimeError("scrollAreaWidgetContents must have a box layout")
        self._layout: QBoxLayout = l
        
        self.refresh_view()
        
    def clear_layout(self):
        if(self._layout is None):
            print("Error: No layout found to clear.")
            return
        while self._layout.count():
            item = self._layout.takeAt(0)          # detach the item from the layout
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)       # hide it immediately
                widget.deleteLater()         # free it when control returns to the event loop
        
    def refresh_view(self):
        self.clear_layout()
        for b in self.bookmarks:
            wg = BookmarkViewItem(b, parent=self)
            wg.edit_requested.connect(self.on_edit_requested)
            wg.delete_requested.connect(self.on_delete_requested)
            self._layout.addWidget(wg)
            
    def on_edit_requested(self, b:Bookmark):
        self.edit_dialog = EditBookmarkDialog(b, parent=self)
        self.edit_dialog.actionSave.connect(self.on_save_requested)
        self.edit_dialog.show()
        
    def on_save_requested(self, updated:Bookmark):
        # Update the bookmark in the list
        for i, bookmark in enumerate(self.bookmarks):
            if bookmark.url == updated.url:
                self.bookmarks[i] = updated
                break
        self.refresh_view()
        self.elementSaved.emit()
        self.edit_dialog.close()

    def on_delete_requested(self, b:Bookmark):
        print(f"Delete requested for bookmark: {b.url}")
        self.delete_requested.emit(b)
        
        
        
            
    