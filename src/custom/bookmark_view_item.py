from functools import partial

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QSizePolicy, QStyle
)
from PySide6.QtCore import Qt, Signal

from bookmarks import Bookmark
from custom.elided_label import ElidedLabel

from utils import human, fmt_time, open_file

class BookmarkViewItem(QWidget):
    
    edit_requested = Signal(Bookmark)
    delete_requested = Signal(Bookmark)
    
    def __init__(self, b:Bookmark,parent = None):
        super().__init__(parent)
        
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 4, 8, 4)
        self._layout.setSpacing(2)
        
        self.__title_label = QLabel("**{title}**".format(title=b.title), textFormat=Qt.TextFormat.MarkdownText)
        self.__title_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.__title_label.setStyleSheet("font-style: bold;")
        self.__desc_label = QLabel(b.desc)
        self.__desc_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.__desc_label.setWordWrap(True)
        self.__url_label = ElidedLabel(b.url)
        self.__url_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        self.__edit_button = QPushButton("")
        self.__edit_button.setIcon(QIcon.fromTheme("document-edit"))
        self.__edit_button.clicked.connect(
            partial(self.edit_requested.emit, b)
        )
        self.__delete_button = QPushButton("")
        self.__delete_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_TrashIcon")))
        self.__delete_button.clicked.connect(
            partial(self.delete_requested.emit, b)
        )
        
        self._layout.addWidget(self.__title_label)
        self._layout.addWidget(self.__desc_label)
        self._layout.addWidget(self.__url_label)
        
        buttons_row = QHBoxLayout()
        buttons_row.addStretch()
        buttons_row.addWidget(self.__edit_button)
        buttons_row.addWidget(self.__delete_button)
        
        self._layout.addLayout(buttons_row)
    
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self._layout.addWidget(line)
