from PySide6.QtWidgets import QDialog, QMessageBox, QWidget
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, Qt

from pathlib import Path
import logging, sys

from settings import *
from profiles import *
from ui.ui_profile_selection import Ui_ProfileSelectionWidget

from views.profile_creator_wizard import ProfileCreatorWizard

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from profiles import *

class ProfileSelectionWidget(QWidget):
    
    profileSelected = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProfileSelectionWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":/App Icons/otus_logo.svg"))
        logger.info("Profile Slection Screen Opened")
        
        self.ui.loginButton.clicked.connect(self.onLoginButtonClicked)
        self.ui.guestProfileButton.clicked.connect(self.onGuestButtonClicked)
        self.ui.newProfileButton.clicked.connect(self.onCreateProfileButtonClicked)
        
        self.ui.usersIcon.setPixmap(QIcon(":/App Icons/otus-users.svg").pixmap(64, 64))
    
        self.__gfs = PyGocryptfs()
        
        self.refreshProfiles()

    def refreshProfiles(self):
        profiles = get_profiles()
        shown_profiles = 0
        self.ui.profilesComboBox.clear()
        for elem in profiles.values():
            if not elem.get("hidden", False):
                self.ui.profilesComboBox.addItem(elem["name"])
                shown_profiles += 1
                        
        if shown_profiles > 0:
            self.ui.profilesComboBox.setCurrentIndex(0)
    
    def onLoginButtonClicked(self):
        profile_name = self.ui.profilesComboBox.currentText()
        password = self.ui.passwordField.text()
        self.ui.passwordField.clear()
        profile = get_profile_by_name(profile_name)
        if not profile:
            logger.error("Profile not found for name: %s", profile_name)
            return
        
        print(profile)
        profile_id = profile["uid"]
        if not profile_id:
            logger.error("Profile ID not found for name: %s", profile_name)
            return

        auth_real = profile.get("auth", None)
        if not auth_real or auth_real == "None":
            logger.info("Profile selected: %s", profile_name)
            self.profileSelected.emit(profile_id)
            #If profile is not protected, emit loginRequested signal. The function terminates here.
            return
        
        if not check_password(profile_name, password):
            logger.warning("Incorrect password for profile: %s", profile_name)
            QMessageBox.warning(self, "Incorrect Password", "The password you entered is incorrect. Please try again.")
            self.ui.passwordField.clear()
            self.ui.passwordField.setFocus()
            self.ui.passwordField.setPlaceholderText("Incorrect password. Try again.")
            return
        
        logger.info("Profile selected: %s", profile_name)
        logger.info("Decrypting profile...")
        
        try:
            conf = KEYS_DIR / f"{profile_id}.conf"
            cipher = PROFILES_DIR / profile_id
            mnt = str(MOUNT_POINT).format(uid=profile_id)   
            self.__gfs.mount(conf, cipher, mnt, password)
        except GocryptfsNotInstalledError or MissingDependenciesError as e:
            logger.error("Gocryptfs is not installed or missing dependencies. Please install it and try again.")
            QMessageBox.critical(
                self,
                "Fatal Error",
                "Gocryptfs is not installed or missing dependencies. Please install it and try again.\nDetais: {error}".format(error=str(e)),
            )
            return
        except GocryptfsError as e:
            QMessageBox.critical(
                self,
                "Fatal Error",
                "Unable to decrypt the profile. Please check your password and try again.\nDetails: {error}".format(error=str(e)),
            )
            return
        except Exception as e:
            logger.error("An unexpected error occurred while decrypting the profile: %s", str(e))
            QMessageBox.critical(
                self,
                "Fatal Error",
                "An unexpected error occurred while decrypting the profile. Please try again.",
            )
            return
        
        self.profileSelected.emit(profile_id)
        
    def onGuestButtonClicked(self):
        self.profileSelected.emit("Otus Guest")
        
    def onCreateProfileButtonClicked(self):
        wizard = ProfileCreatorWizard(self)

        wizard.profileCreated.connect(self.onProfileCreated)
        wizard.loginRequested.connect(self.onLoginRequested)

        wizard.exec()
        
    def onProfileCreated(self, profile_id: str):
        logger.info("Profile created with ID: %s", profile_id)
        self.refreshProfiles()

    def onLoginRequested(self, profile_id: str):
        logger.info("Login requested for profile: %s", profile_id)
        self.profileSelected.emit(profile_id)