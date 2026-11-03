from PySide6.QtWidgets import (
    QFileDialog, QListWidgetItem, QMessageBox, QProgressDialog, QWidget
)
from PySide6.QtCore import QUrl, Qt, QThread, Signal
from PySide6.QtGui import QIcon
from pathlib import Path

from settings import OTUS_ICON_PACK

from ui.ui_package_manager import Ui_OtusPackageManager

from package_manager import (
    PackageManager,
    InstallError,
    CorruptedPackage,
    InvalidManifest,
    PackageTypeNotSupported,
    PackageNotFound,
    PackageAlreadyInstalled,
    PackageNotInstalled
)

DEFAULT_ICON = OTUS_ICON_PACK + "otus-pkg-default.png"


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

        self._install_thread: InstallThread | None = None
        self._progress_dialog: QProgressDialog | None = None
        self._install_error: str | None = None

        self.ui.installPackageButton.clicked.connect(self.on_install_package)
        self.ui.searchBox.textChanged.connect(self.filter_packages)
        self.ui.packageList.currentItemChanged.connect(self.show_package_details)
        self.ui.packageList.itemDoubleClicked.connect(self.open_selected_app)
        self.ui.uninstallPackageButton.clicked.connect(self.uninstall_selected_package)
        self.populate_packages()

    # ------------------------------------------------------------------
    # Installed packages list
    # ------------------------------------------------------------------
    def populate_packages(self):
        package_list = self.ui.packageList
        package_list.clear()
        for pkg in self.pkgs_manager.get_installed_packages():
            icon = QIcon(pkg.icon) if pkg.icon else QIcon()
            if icon.isNull():
                icon = QIcon(DEFAULT_ICON)
            item = QListWidgetItem(icon, f"{pkg.name}\n{pkg.version}", package_list)
            item.setData(Qt.ItemDataRole.UserRole, pkg)
        self.filter_packages(self.ui.searchBox.text())

    def filter_packages(self, text: str):
        query = text.casefold().strip()
        for index in range(self.ui.packageList.count()):
            item = self.ui.packageList.item(index)
            package = item.data(Qt.ItemDataRole.UserRole)
            searchable = f"{package.name} {package.id} {package.description}".casefold()
            item.setHidden(bool(query and query not in searchable))

    def show_package_details(self, current: QListWidgetItem | None, _previous: QListWidgetItem | None):
        if current is None:
            self.ui.detailsText.clear()
            self.ui.uninstallPackageButton.setEnabled(False)
            return
        package = current.data(Qt.ItemDataRole.UserRole)
        self.ui.detailsText.setPlainText(
            f"Name: {package.name}\n"
            f"ID: {package.id}\n"
            f"Version: {package.version}\n"
            f"Type: {package.type}\n"
            f"Authors: {', '.join(package.authors)}\n"
            f"License: {package.license}\n\n"
            f"{package.description}"
        )
        self.ui.uninstallPackageButton.setEnabled(True)

    def uninstall_selected_package(self):
        item = self.ui.packageList.currentItem()
        if item is None:
            return

        package = item.data(Qt.ItemDataRole.UserRole)
        answer = QMessageBox.question(
            self,
            "Uninstall Package",
            f"Are you sure you want to uninstall '{package.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.pkgs_manager.uninstall_package(package.id)
        except (PackageNotFound, PackageNotInstalled) as error:
            QMessageBox.critical(self, "Package Uninstallation Error", str(error))
            return
        except OSError as error:
            QMessageBox.critical(self, "Package Uninstallation Error", str(error))
            return

        self.populate_packages()

    def open_selected_app(self, item: QListWidgetItem):
        package = item.data(Qt.ItemDataRole.UserRole)
        if package.type == "app":
            self.open_app(package)

    def open_app(self, package):
        if package.directory is None:
            QMessageBox.warning(self, "Open Application", "Application directory is missing.")
            return
        if package.meta.get("runtime") != "self":
            QMessageBox.warning(self, "Open Application", "Unsupported application runtime.")
            return

        entrypoint = package.meta.get("entrypoint")
        if not entrypoint:
            QMessageBox.warning(self, "Open Application", "Application entrypoint is missing.")
            return

        app_directory = Path(package.directory).resolve()
        entrypoint_path = (app_directory / entrypoint).resolve()
        if not entrypoint_path.is_relative_to(app_directory) or not entrypoint_path.is_file():
            QMessageBox.warning(self, "Open Application", "Application entrypoint is invalid.")
            return

        main_window = self.window()
        new_tab = getattr(main_window, "new_tab", None)
        if not callable(new_tab):
            QMessageBox.warning(self, "Open Application", "The browser window is unavailable.")
            return
        new_tab(QUrl.fromLocalFile(str(entrypoint_path)).toString())

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
        try:
            self._install_error = None
            thread = InstallThread(self.pkgs_manager, file_path, parent=self)
            thread.progress.connect(self._on_install_progress)
            thread.failed.connect(self._on_install_failed)
            thread.finished.connect(self._on_install_finished)
            self._install_thread = thread
            thread.start()
        except InvalidManifest as e:
            dialog.close()
            QMessageBox.critical(self, "Package Installation Error", str(e))
        except PackageTypeNotSupported as e:
            dialog.close()
            QMessageBox.critical(self, "Package Installation Error", str(e))
        except PackageAlreadyInstalled as e:
            dialog.close()
            QMessageBox.critical(self, "Package Installation Error", str(e))
        except PackageNotInstalled as e:
            dialog.close()
            QMessageBox.critical(self, "Package Installation Error", f"Package not installed: {str(e)}")
        except CorruptedPackage as e:
            dialog.close()
            QMessageBox.critical(self, "Package Installation Error", f"Corrupted package: {str(e)}")

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