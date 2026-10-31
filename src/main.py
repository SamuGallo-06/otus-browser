# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Samuele Gallicani

# main.py

#PySide6
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QGuiApplication, QIcon

#Python Modules
import sys, logging
from gettext import gettext as gtr
from datetime import datetime
from pathlib import Path
import typer

#Custom Modules
from views.main_window import MainWindow
from views.profile_screen import ProfileSelectionWidget
from profiles import OtusProfile, get_profile_by_id
from pygocryptfs import GocryptfsError, PyGocryptfs
import settings
from ui import resources_rc
from user_settings import (
    AppSettings,
    ProfileSettings,
    SettingsManager,
    init_app_settings,
)


logger = logging.getLogger(__name__)
def setupLogger():
    global logger
    
    date = datetime.now().strftime("%Y-%m-%d")
    clock = datetime.now().strftime("%H-%M-%S")
    dt = "{date} {clock}".format(date=date, clock=clock) 
    
    logdir: Path = settings.LOG_FILE_PATH / date
    logdir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(filename=logdir / f"otus-{clock}.log", level=logging.INFO)
    logger.info(gtr("-----------------------| Welcome to Otus Browser |-----------------------"))
    logger.info(gtr("Date and Time: {datetime}").format(datetime=dt))


class OtusApp:
    def __init__(self, app_settings: SettingsManager[AppSettings], url: str | None = None):
        self.app_settings = app_settings
        self.login = None
        self.main_window = None
        self.profile_settings: SettingsManager[ProfileSettings] | None = None
        self.start_url = url

    def start(self):
        if self.app_settings.settings.ask_for_profile_choose:
            self.login = ProfileSelectionWidget()
            self.login.profileSelected.connect(self.openMainWindow)
            self.login.show()
        else:
            logger.info(gtr("Skipped profile selection"))
            default_profile = self.app_settings.settings.default_profile
            profile = get_profile_by_id(default_profile)
            if profile is None:
                profile = OtusProfile(
                    uid=default_profile,
                    name=default_profile,
                )
            self.openMainWindow(profile)

    def openMainWindow(self, profile: OtusProfile):
        logger.info(gtr("Opening main window"))
        self.profile_settings = SettingsManager(
            profile.storage_path / "settings.ini",
            ProfileSettings,
            parent=QApplication.instance(),
        )
        self.main_window = MainWindow(
            profile=profile,
            profile_settings=self.profile_settings,
            start_url=self.start_url
        )
        self.main_window.exitRequested.connect(self.exitApplication)
        self.main_window.closed.connect(self.unmountProfile)
        self.main_window.show()
        if self.login is not None:
            self.login.close() 
            self.login.deleteLater()
            self.login = None
            
    def exitApplication(self):
        logger.info(gtr("Exiting application"))
        if self.main_window is not None:
            self.main_window.close()
            self.main_window.deleteLater()
            self.main_window = None

    def unmountProfile(self, profile: OtusProfile):
        if self.profile_settings is not None:
            self.profile_settings.close()
        if not profile.encrypted or profile.mountpoint is None:
            self.profile_settings = None
            return

        QTimer.singleShot(0, lambda: self._unmountProfile(profile))

    def _unmountProfile(self, profile: OtusProfile):
        try:
            PyGocryptfs().unmount(profile.mountpoint) #type: ignore
            logger.info(gtr("Unmounted encrypted profile: %s"), profile.uid)
            profile.mountpoint = None
            self.profile_settings = None
        except GocryptfsError:
            logger.exception(gtr("Unable to unmount encrypted profile: %s"), profile.uid)
            
def apply_theme(app: QApplication, manager: SettingsManager[AppSettings]) -> None:
    scheme = settings.AVAILABLE_THEMES.get(
        manager.settings.theme,
        Qt.ColorScheme.Unknown,
    )
    app.styleHints().setColorScheme(scheme)
    
cli = typer.Typer()

@cli.command()
def main(
    url: str | None = typer.Argument(None, help=gtr("")),
):
    setupLogger()
    
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Otus Browser")
    app.setWindowIcon(QIcon(settings.OTUS_ICON_PACK + "otus_logo.svg"))
    app.setApplicationName("otus-browser")
    app.setApplicationVersion("0.0.1")
        
    app_settings = init_app_settings(settings.SETTINGS_PATH, parent=app)
    apply_theme(app, app_settings)
    app_settings.settingsChanged.connect(lambda: apply_theme(app, app_settings))
    

    otus = OtusApp(app_settings, url)
    otus.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    cli()
    
