from PySide6.QtCore import QLine, Qt, Signal
from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QSizePolicy, QStyle
from pathlib import Path
from functools import partial
from downloads import Download

from custom.elided_label import ElidedLabel

from utils import human, fmt_eta, open_file

## TODO: implement the progress bar for in-progress downloads
## TODO: implement the pause/resume/cancel button for in-progress downloads

class DownloadViewItem(QWidget):
    
    deleteRequested = Signal(Download)
    copySourceUrlRequested = Signal(Download)
    pauseRequested = Signal(Download)
    resumeRequested = Signal(Download)
    cancelRequested = Signal(Download)
    
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
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self._layout.addWidget(line)
        
    def define_state(self):
        if(self.download.status == "DownloadInProgress"):
            self.__pbar = QProgressBar(self)
            self.__update_progress()
            self._layout.addWidget(self.__pbar)
        elif(self.download.status == "DownloadCanceled"):
            self.__statusLabel = QLabel(" Status: Canceled")
            self._layout.addWidget(self.__statusLabel)
        elif(self.download.status == "DownloadCompleted"):
            self.__statusLabel = QLabel(" Status: Completed")
            self._layout.addWidget(self.__statusLabel)
            if(not Path(self.download.filepath).exists()):
                self.__statusLabel.setText(" File has been moved or deleted.")
                self.__statusLabel.setStyleSheet("font-style: italic;")
        elif(self.download.status == "DownloadInterrupted"):
            self.__statusLabel = QLabel(" Status: Failed")
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
        
        self.__copy_source_button = QPushButton("Copy Source", self)
        self.__copy_source_button.setToolTip("Copy the source URL to the clipboard")
        self.__copy_source_button.clicked.connect(
            partial(self.copySourceUrlRequested.emit, self.download)
        )
        self._layout.addWidget(self.__copy_source_button, alignment=Qt.AlignmentFlag.AlignRight)

        if self.download.status == "DownloadInProgress":
            self.__pause_button = QPushButton("Pause", self)
            self.__pause_button.clicked.connect(self.__toggle_pause)
            self._layout.addWidget(self.__pause_button, alignment=Qt.AlignmentFlag.AlignRight)

            self.__cancel_button = QPushButton("Cancel", self)
            self.__cancel_button.clicked.connect(
                partial(self.cancelRequested.emit, self.download)
            )
            self._layout.addWidget(self.__cancel_button, alignment=Qt.AlignmentFlag.AlignRight)
        
        if(self.download.status == "DownloadCompleted" and Path(self.download.filepath).exists()):
            self.__open_file_button = QPushButton("Open", self)
            self.__open_file_button.setToolTip("Open this file with the default program")
            self.__open_file_button.clicked.connect(
                lambda: open_file(self.download.filepath)
            )
            self._layout.addWidget(self.__open_file_button, alignment=Qt.AlignmentFlag.AlignRight)

    def __toggle_pause(self):
        if self.__pause_button.text() == "Resume":
            self.resumeRequested.emit(self.download)
        else:
            self.pauseRequested.emit(self.download)

    def __update_progress(self):
        if self.download.total_bytes > 0:
            progress = min(
                100,
                int(self.download.received_bytes * 100 / self.download.total_bytes),
            )
            self.__pbar.setRange(0, 100)
            self.__pbar.setValue(progress)
        else:
            self.__pbar.setRange(0, 0)

    def update_download(self, download: Download):
        if download.ident != self.download.ident:
            return

        self.download = download
        if hasattr(self, "_DownloadViewItem__pbar"):
            self.__update_progress()
        if hasattr(self, "_DownloadViewItem__pause_button"):
            self.__pause_button.setText(
                "Resume" if download.status == "DownloadPaused" else "Pause"
            )