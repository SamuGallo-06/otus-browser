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


if __name__ == "__main__":
    setupLogger()
    
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Otus Browser")
    app.setWindowIcon(QIcon(":/App Icons/otus_logo.png"))
    app.setApplicationName("otus-browser")
    app.setApplicationVersion("0.0.1")

    profile_name = "OtusProfile"  # Default profile name
    
    if(settings.ASK_FOR_PROFILE_CHOOSE):
        logger.info("Profile selection is not implemented yet")
        logger.info("Using default profile: OtusProfile")
    else:
        logger.info("Skipped profile selection, using last used profile: OtusProfile")
        profile_name = "OtusProfile"
        
    w = MainWindow(profile_name=profile_name)
    w.show()
    sys.exit(app.exec())
    
