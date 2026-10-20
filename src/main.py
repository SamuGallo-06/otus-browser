# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Samuele Gallicani

# main.py

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from views.main_window import MainWindow

import settings

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Otus Browser")
    app.setWindowIcon(QIcon(":/App Icons/otus_logo.png"))
    app.setApplicationName("otus-browser")
    app.setApplicationVersion("0.0.1")

    profile_name = "OtusProfile"  # Default profile name
    
    if(settings.ASK_FOR_PROFILE_CHOOSE):
        profile_name = str(input("Profile selection is not implemented yet. Please enter the profile name (default: OtusProfile): "))
        if not profile_name:
            print("Using default profile: OtusProfile")
            profile_name = "OtusProfile"
        else:
            profile_name = "OtusProfile"  # For now, we will still use the default profile since profile selection is not implemented yet.
    else:
        print("Using default profile: OtusProfile")
        profile_name = "OtusProfile"
        
    w = MainWindow(profile_name=profile_name)
    w.show()
    sys.exit(app.exec())