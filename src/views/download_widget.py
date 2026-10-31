from PySide6.QtCore import Qt, QElapsedTimer, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox, QWidget
from downloads import Download, DownloadManager
from ui.ui_download import Ui_DownloadWidget

from utils import human, fmt_eta

class DownloadWidget(QWidget):
    def __init__(
        self, download: Download, download_manager: DownloadManager, parent=None
    ):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.Window)
        self.ui = Ui_DownloadWidget()
        self.ui.setupUi(self)
        self.download = download
        self.download_manager = download_manager

        # PlainText: un QLabel interpreta HTML, e il nome file è input non fidato
        self.ui.headerLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.ui.headerLabel.setText(
            self.tr("Downloading: {filename} from {host}").format(
                filename=download.filename,
                host=QUrl(download.source).host(),
            )
        )
        self.ui.progressBar.setValue(0)

        self._clock = QElapsedTimer(); self._clock.start()
        self._last_ms, self._last_bytes, self._speed = 0, 0, 0.0

        download_manager.downloadUpdated.connect(self.update_download)
        self.ui.pauseDownloadButton.clicked.connect(self.togglePause)
        self.ui.cancelDownloadButton.clicked.connect(self.toggleCancel)
        self.ui.openDownloadFolderButton.clicked.connect(self.openFolder)
        self.refresh()
    
    def refresh(self):
        now = self._clock.elapsed()
        elapsed = now - self._last_ms
        if elapsed <= 0:
            return
        received, total = self.download.received_bytes, self.download.total_bytes

        inst = (received - self._last_bytes) / (elapsed / 1000)
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
            self.tr(
                "Downloaded {received} / {total}\n"
                "Transfer rate: {rate}/s\n"
                "Estimated time left: {eta}"
            ).format(
                received=human(received),
                total=human(total) if total > 0 else "?",
                rate=human(self._speed),
                eta=fmt_eta(eta),
            )
        )
        
    def togglePause(self):
        if self.download.paused:
            self.download_manager.resume(self.download)
            self.ui.pauseDownloadButton.setText(self.tr("Pause"))
        else:
            self.download_manager.pause(self.download)
            self.ui.pauseDownloadButton.setText(self.tr("Resume"))

    def openFolder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.download.filepath.parent)))
        
    def toggleCancel(self):
        if self.download.status in {"DownloadCompleted", "DownloadCancelled", "DownloadInterrupted"}:
            self.close()
        else:
            result = QMessageBox.warning(
                self,
                self.tr("Cancel download"),
                self.tr("Are you sure you want to cancel the download?"),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if result == QMessageBox.StandardButton.Yes:
                self.download_manager.cancel(self.download)

    def onStateChanged(self):
        if self.download.status == "DownloadCompleted":
            self.ui.progressBar.setRange(0, 100)
            self.ui.progressBar.setValue(100)
            self.ui.detailsLabel.setText(self.tr("Download completed"))
        elif self.download.status == "DownloadCancelled":
            self.ui.detailsLabel.setText(self.tr("Download canceled"))
            self.close()
        elif self.download.status == "DownloadInterrupted":
            self.ui.detailsLabel.setText(self.tr("Download interrupted"))
        else:
            return                       # DownloadInProgress / Requested
        self.ui.pauseDownloadButton.setEnabled(False)
        self.ui.cancelDownloadButton.setEnabled(False)

    def update_download(self, download: Download):
        if download.ident != self.download.ident:
            return
        self.download = download
        self.refresh()
        if self.download.status not in {
            "DownloadCompleted", "DownloadCancelled", "DownloadInterrupted"
        }:
            self.ui.pauseDownloadButton.setText(
                self.tr("Resume") if download.paused else self.tr("Pause")
            )
        self.onStateChanged()