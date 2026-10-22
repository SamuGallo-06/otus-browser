# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Samuele Gallicani

# main.py

#PySide6
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

#Python Modules
import sys, logging
from datetime import datetime
from pathlib import Path

#Custom Modules
from views.main_window import MainWindow
from views.profile_screen import ProfileSelectionWidget
import settings

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
            self.openMainWindow(settings.DEFAULT_PROFILE)

    def openMainWindow(self, profile_id: str):
        logger.info("Opening main window")
        self.main_window = MainWindow(profile_id=profile_id)
        self.main_window.show()
        if self.login is not None:
            self.login.close() 
            self.login.deleteLater()
            self.login = None


if __name__ == "__main__":
    setupLogger()

    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Otus Browser")
    app.setWindowIcon(QIcon(":/App Icons/otus_logo.png"))
    app.setApplicationName("otus-browser")
    app.setApplicationVersion("0.0.1")

    otus = OtusApp()
    otus.start()
    sys.exit(app.exec())
    
