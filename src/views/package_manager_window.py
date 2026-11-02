from PySide6.QtWidgets import (
    QFileDialog, QGridLayout, QLabel, QMessageBox, QProgressDialog, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt, QSize, QThread, Signal
from PySide6.QtGui import QIcon

from settings import OTUS_ICON_PACK

from ui.ui_package_manager import Ui_OtusPackageManager

from package_manager import PackageManager

ITEM_WIDTH = 110
ICON_SIZE = QSize(64, 64)
DEFAULT_ICON = OTUS_ICON_PACK + "otus-pkg-default.png"


class PackageItem(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(ITEM_WIDTH)

        # The layout MUST be installed on the widget (passing `self`), otherwise the
        # labels are never reparented to it and they are never shown.
        self._layout = QVBoxLayout(self)

        self.pixmapLabel = QLabel("")
        self.pixmapLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pixmapLabel.setPixmap(QIcon(DEFAULT_ICON).pixmap(ICON_SIZE))

        self.nameLabel = QLabel("")
        self.nameLabel.setTextFormat(Qt.TextFormat.RichText)
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setWordWrap(True)

        self._layout.addWidget(self.pixmapLabel)
        self._layout.addWidget(self.nameLabel)


class InstallThread(QThread):
    """Runs PackageManager.install_package off the GUI thread."""

    progress = Signal(str, int)
    failed = Signal(str)

    def __init__(self, manager: PackageManager, package_path: str, parent=None):
        super().__init__(parent)
        self._manager = manager
        self._package_path = package_path

    def run(self):
        # Signal-to-signal connection: the progress is delivered to the GUI thread
        # through a queued connection, so the dialog can repaint while we copy files.
        self._manager.progressUpdated.connect(self.progress)
        try:
            self._manager.install_package(self._package_path)
        except Exception as error:
            self.failed.emit(str(error))
        finally:
            self._manager.progressUpdated.disconnect(self.progress)


class OtusPackageManager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_OtusPackageManager()
        self.setWindowFlag(Qt.WindowType.Window)
        self.ui.setupUi(self)
        self.pkgs_manager = PackageManager()

        layout = self.ui.scrollAreaWidgetContents.layout()
        if not isinstance(layout, QGridLayout):
            raise RuntimeError("scrollAreaWidgetContents must have a grid layout")
        self.pkgs_layout: QGridLayout = layout
        self.pkgs_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self._columns = 0
        self._install_thread: InstallThread | None = None
        self._progress_dialog: QProgressDialog | None = None
        self._install_error: str | None = None

        self.ui.installPackageButton.clicked.connect(self.on_install_package)
        self.populate_packages()

    # ------------------------------------------------------------------
    # Installed packages grid
    # ------------------------------------------------------------------
    def _compute_columns(self) -> int:
        spacing = self.pkgs_layout.horizontalSpacing()
        spacing = max(spacing, 0)
        viewport_width = self.ui.scrollArea.viewport().width()
        return max(1, viewport_width // (ITEM_WIDTH + spacing))

    def populate_packages(self):
        self.clear_layout()

        self._columns = self._compute_columns()

        for index, pkg in enumerate(self.pkgs_manager.get_installed_packages()):
            row = index // self._columns
            col = index % self._columns

            pkg_item = PackageItem()
            pkg_item.nameLabel.setText(f"<b>{pkg.name}</b><br/>{pkg.version}")
            icon = QIcon(pkg.icon) if pkg.icon else QIcon()
            if icon.isNull():
                icon = QIcon(DEFAULT_ICON)
            pkg_item.pixmapLabel.setPixmap(icon.pixmap(ICON_SIZE))

            self.pkgs_layout.addWidget(pkg_item, row, col)

    def clear_layout(self):
        while self.pkgs_layout.count():
            item = self.pkgs_layout.takeAt(0)  # detach the item from the layout
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)  # hide it immediately
                widget.deleteLater()  # free it when control returns to the event loop

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Re-flow the grid only when the number of columns actually changes
        if self._compute_columns() != self._columns:
            self.populate_packages()

    # ------------------------------------------------------------------
    # Installation
    # ------------------------------------------------------------------
    def on_install_package(self):
        if self._install_thread is not None:
            return  # an installation is already running

        file_path = QFileDialog.getOpenFileName(
            self, "Select Package File", "", "Otus Package Files (*.otuspkg)"
        )[0]
        if not file_path:
            return

        dialog = QProgressDialog("Installing package...", "", 0, 100, self)
        dialog.setWindowTitle("Installing Package")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.setMinimumDuration(0)
        # The range is 0-100: with 0-0 the dialog is "busy" and setValue(0) would
        # already count as "finished" and hide it. Also, close it by hand only.
        dialog.setAutoClose(False)
        dialog.setAutoReset(False)
        # install_package cannot be interrupted halfway, so there is nothing to cancel
        dialog.setCancelButton(None)  # type: ignore[arg-type]
        dialog.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        dialog.setValue(0)
        dialog.show()
        self._progress_dialog = dialog

        self._install_error = None
        thread = InstallThread(self.pkgs_manager, file_path, parent=self)
        thread.progress.connect(self._on_install_progress)
        thread.failed.connect(self._on_install_failed)
        thread.finished.connect(self._on_install_finished)
        self._install_thread = thread
        thread.start()

    def _on_install_progress(self, message: str, value: int):
        if self._progress_dialog is not None:
            self._progress_dialog.setLabelText(message)
            self._progress_dialog.setValue(value)

    def _on_install_failed(self, message: str):
        self._install_error = message

    def _on_install_finished(self):
        # Runs in the GUI thread, after run() has returned
        if self._progress_dialog is not None:
            self._progress_dialog.close()
            self._progress_dialog.deleteLater()
            self._progress_dialog = None

        if self._install_thread is not None:
            self._install_thread.deleteLater()
            self._install_thread = None

        if self._install_error is not None:
            QMessageBox.critical(self, "Package Installation Error", self._install_error)
        else:
            self.populate_packages()