from bookmarks import Bookmark

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal

from ui.ui_edit_bookmark import Ui_EditBookmarkDialog


class EditBookmarkDialog(QWidget):
    
    actionSave = Signal(Bookmark)
    
    def __init__(self, bookmark: Bookmark, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.Window)
        self.bookmark = bookmark
        self.ui = Ui_EditBookmarkDialog()
        self.ui.setupUi(self)
        self.ui.titleField.setText(bookmark.title)
        self.ui.urlField.setText(bookmark.url)
        self.ui.descriptionField.setText(bookmark.desc)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)

    def save(self):
        self.actionSave.emit(Bookmark(
            url=self.ui.urlField.text(),
            title=self.ui.titleField.text(),
            desc=self.ui.descriptionField.text(),
            parent=self.bookmark.parent
        ))
        self.close()