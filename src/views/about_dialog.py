from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog
from ui.ui_about_dialog import Ui_AboutDialog

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.Window)    