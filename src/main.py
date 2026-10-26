# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Samuele Gallicani

# main.py

#PySide6
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QGuiApplication, QIcon

#Python Modules
import sys, logging
from datetime import datetime
from pathlib import Path

#Custom Modules
from views.main_window import MainWindow
from views.profile_screen import ProfileSelectionWidget
from profiles import OtusProfile, get_profile_by_id
from pygocryptfs import GocryptfsError, PyGocryptfs
import settings
from ui import resources_rc

logger = logging.getLogger(__name__)
def setupLogger():
    global logger
    
    date = datetime.now().strftime("%d-%m-%Y")
    clock = datetime.now().strftime("%H:%M:%S") 
    dt = "{date} {clock}".format(date=date, clock=clock) 
    
    logdir: Path = settings.LOG_FILE_PATH / date
    logdir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(filename=logdir / f"otus-{clock}.log", level=logging.INFO)
    logger.info("-----------------------| Welcome to Otus Browser |-----------------------")
    logger.info("Date and Time: {datetime}".format(datetime=dt))


class OtusApp:
    def __init__(self):
        self.login = None
        self.main_window = None


    def start(self):
        if settings.ASK_FOR_PROFILE_CHOOSE:
            self.login = ProfileSelectionWidget()
            self.login.profileSelected.connect(self.openMainWindow)
            self.login.show()
        else:
            logger.info("Skipped profile selection")
            profile = get_profile_by_id(settings.DEFAULT_PROFILE)
            if profile is None:
                profile = OtusProfile(
                    uid=settings.DEFAULT_PROFILE,
                    name=settings.DEFAULT_PROFILE,
                )
            self.openMainWindow(profile)

    def openMainWindow(self, profile: OtusProfile):
        logger.info("Opening main window")
        self.main_window = MainWindow(profile=profile)
        self.main_window.exitRequested.connect(self.exitApplication)
        self.main_window.closed.connect(self.unmountProfile)
        self.main_window.show()
        if self.login is not None:
            self.login.close() 
            self.login.deleteLater()
            self.login = None
            
    def exitApplication(self):
        logger.info("Exiting application")
        if self.main_window is not None:
            self.main_window.close()
            self.main_window.deleteLater()
            self.main_window = None

    def unmountProfile(self, profile: OtusProfile):
        if not profile.encrypted or profile.mountpoint is None:
            return

        QTimer.singleShot(0, lambda: self._unmountProfile(profile))

    def _unmountProfile(self, profile: OtusProfile):
        try:
            PyGocryptfs().unmount(profile.mountpoint) #type: ignore
            logger.info("Unmounted encrypted profile: %s", profile.uid)
            profile.mountpoint = None
        except GocryptfsError:
            logger.exception("Unable to unmount encrypted profile: %s", profile.uid)
            
def apply_theme(theme: str) -> None:
    hints = QGuiApplication.styleHints()
    hints.setColorScheme(settings.AVAILABLE_THEMES.get(theme.lower(), Qt.ColorScheme.Light))


if __name__ == "__main__":
    setupLogger()

    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Otus Browser")
    app.setWindowIcon(QIcon(":/resources/otus_logo.png"))
    app.setApplicationName("otus-browser")
    app.setApplicationVersion("0.0.1")
    
    theme = settings.THEME
    apply_theme(theme)

    otus = OtusApp()
    otus.start()
    sys.exit(app.exec())
    
