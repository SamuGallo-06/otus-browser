from PySide6.QtCore import Qt, QElapsedTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox, QMessageBox, QWidget
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest as DR
from ui.ui_download import Ui_DownloadWidget

from utils import human, fmt_eta

class DownloadWidget(QWidget):
    def __init__(self, request: DR, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.Window)
        self.ui = Ui_DownloadWidget()
        self.ui.setupUi(self)
        self.request = request

        # PlainText: un QLabel interpreta HTML, e il nome file è input non fidato
        self.ui.headerLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.ui.headerLabel.setText(
            f"Downloading: {request.downloadFileName()} from {request.url().host()}")
        self.ui.progressBar.setValue(0)

        self._clock = QElapsedTimer(); self._clock.start()
        self._last_ms, self._last_bytes, self._speed = 0, 0, 0.0

        request.receivedBytesChanged.connect(self.refresh)
        request.totalBytesChanged.connect(self.refresh)
        request.stateChanged.connect(self.onStateChanged)
        self.ui.pauseDownloadButton.clicked.connect(self.togglePause)
        self.ui.cancelDownloadButton.clicked.connect(self.toggleCancel)
        self.ui.openDownloadFolderButton.clicked.connect(self.openFolder)
    
    def refresh(self):
        now = self._clock.elapsed()
        if now - self._last_ms < 500:
            return
        received, total = self.request.receivedBytes(), self.request.totalBytes()

        inst = (received - self._last_bytes) / ((now - self._last_ms) / 1000)
        self._speed = inst if self._speed == 0 else 0.7 * self._speed + 0.3 * inst
        self._last_ms, self._last_bytes = now, received

        bar = self.ui.progressBar
        if total > 0:
            bar.setRange(0, 100)
            bar.setValue(int(received * 100 / total))
            eta = (total - received) / self._speed if self._speed > 0 else None
        else:
            bar.setRange(0, 0)          # indeterminata se la dimensione è ignota
            eta = None

        self.ui.detailsLabel.setText(
            f"Downloaded {human(received)} / {human(total) if total > 0 else '?'}\n"
            f"Transfer rate: {human(self._speed)}/s\n"
            f"Estimated time left: {fmt_eta(eta)}")
        
    def togglePause(self):
        if self.request.isPaused():
            self.request.resume()
            self.ui.pauseDownloadButton.setText("Pause")
        else:
            self.request.pause()
            self.ui.pauseDownloadButton.setText("Resume")

    def openFolder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.request.downloadDirectory()))
        
    def toggleCancel(self):
        if self.request.isFinished():
            self.close()
        else:
            result = QMessageBox.warning(
                self,
                "Cancel download", 
                "Are you sure you want to cancel the download?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if result == QMessageBox.StandardButton.Yes:
                self.request.cancel()

    def onStateChanged(self, state):
        S = DR.DownloadState
        if state == S.DownloadCompleted:
            self.ui.progressBar.setRange(0, 100)
            self.ui.progressBar.setValue(100)
            self.ui.detailsLabel.setText("Download completed")
        elif state == S.DownloadCancelled:
            self.ui.detailsLabel.setText("Download canceled")
            self.close()
        elif state == S.DownloadInterrupted:
            self.ui.detailsLabel.setText(
                f"Download interrupted: {self.request.interruptReasonString()}")
        else:
            return                       # DownloadInProgress / Requested
        self.ui.pauseDownloadButton.setEnabled(False)
        self.ui.cancelDownloadButton.setEnabled(False)