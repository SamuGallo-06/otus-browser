from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QSizePolicy, QStyle
from pathlib import Path
from functools import partial
from downloads import Download

from custom.elided_label import ElidedLabel

from utils import human, fmt_eta

## TODO: implement the copy source button
## TODO: implement the open file button
## TODO: implement the progress bar for in-progress downloads
## TODO: implement the pause/resume/cancel button for in-progress downloads

class DownloadViewItem(QWidget):
    
    deleteRequested = Signal(Download)
    
    def __init__(self, d: Download, parent = None):
        super().__init__(parent)
        self.download = d

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 4, 8, 4)
        self._layout.setSpacing(2)
        
        self.__title_label = QLabel("{filename}".format(filename=self.download.filename), textFormat=Qt.TextFormat.MarkdownText)
        self.__title_label.setStyleSheet("QLabel { font-style: bold; }")
        self.__title_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.__source_label = ElidedLabel(self.download.source or "unknown")
        self.__details_label = QLabel(
            "Total Size: {size} · Created at: {time}".format(
                size=human(self.download.total_bytes),
                time=fmt_eta(self.download.timestamp),
            )
        )
        self.__details_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        self._layout.addWidget(self.__title_label)
        self._layout.addWidget(self.__source_label)
        self._layout.addWidget(self.__details_label)
        
        self.define_state()
        self.define_buttons()
        
    def define_state(self):
        if(self.download.status == "DownloadInProgress"):
            self.__pbar = QProgressBar(self)
            self.__pbar.setMaximum(-1)  # Indeterminate state
            self.__pbar.setValue(0)
            self._layout.addWidget(self.__pbar)
        elif(self.download.status == "DownloadCanceled"):
            self.__statusLabel = QLabel("Status: Canceled")
            self._layout.addWidget(self.__statusLabel)
        elif(self.download.status == "DownloadCompleted"):
            self.__statusLabel = QLabel("Status: Completed")
            self._layout.addWidget(self.__statusLabel)
            if(not Path(self.download.filename).exists()):
                self.__statusLabel.setText(" File has been moved or deleted.")
                self.__statusLabel.setStyleSheet("font-style: italic;")
        elif(self.download.status == "DownloadInterrupted"):
            self.__statusLabel = QLabel("Status: Failed")
            self.__statusLabel.setStyleSheet("font-style: italic; color: red;")
            self._layout.addWidget(self.__statusLabel)
            
    def define_buttons(self):
        self.__delete_button = QPushButton("", self)
        self.__delete_button.setIcon(self.style().standardIcon(getattr(QStyle, "SP_TrashIcon")))
        self.__delete_button.setToolTip("Delete this download from history")
        self.__delete_button.clicked.connect(
            partial(self.deleteRequested.emit, self.download)
        )
        self._layout.addWidget(self.__delete_button, alignment=Qt.AlignmentFlag.AlignRight)