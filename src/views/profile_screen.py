from PySide6.QtWidgets import QDialog, QMessageBox, QWidget
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, Qt

from pathlib import Path
import logging, sys
from gettext import gettext as gtr

from settings import *
from profiles import *
from ui.ui_profile_selection import Ui_ProfileSelectionWidget
from ui import resources_rc

from views.profile_creator_wizard import ProfileCreatorWizard

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from profiles import *

class ProfileSelectionWidget(QWidget):
    
    profileSelected = Signal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProfileSelectionWidget()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(OTUS_ICON_PACK + "otus_logo.png"))
        logger.info(gtr("Profile Slection Screen Opened"))
        
        self.ui.loginButton.clicked.connect(self.onLoginButtonClicked)
        self.ui.guestProfileButton.clicked.connect(self.onGuestButtonClicked)
        self.ui.newProfileButton.clicked.connect(self.onCreateProfileButtonClicked)
    
        self.refreshProfiles()

    def refreshProfiles(self):
        profiles = get_profiles()
        shown_profiles = 0
        self.ui.profilesComboBox.clear()
        for elem in profiles.values():
            if not elem.hidden:
                self.ui.profilesComboBox.addItem(elem.name)
                shown_profiles += 1
                        
        if shown_profiles > 0:
            self.ui.profilesComboBox.setCurrentIndex(0)
    
    def onLoginButtonClicked(self):
        profile_name = self.ui.profilesComboBox.currentText()
        password = self.ui.passwordField.text()
        self.ui.passwordField.clear()
        profile = get_profile_by_name(profile_name)
        if not profile:
            logger.error(gtr("Profile not found for name: %s"), profile_name)
            return
        
        if not profile.uid:
            logger.error(gtr("Profile ID not found for name: %s"), profile_name)
            return

        if not profile.auth:
            logger.info(gtr("Profile selected: %s"), profile_name)
            self.profileSelected.emit(profile)
            #If profile is not protected, emit loginRequested signal. The function terminates here.
            return
        
        if not check_password(profile, password):
            logger.warning(gtr("Incorrect password for profile: %s"), profile_name)
            QMessageBox.warning(
                self,
                self.tr("Incorrect Password"),
                self.tr("The password you entered is incorrect. Please try again."),
            )
            self.ui.passwordField.clear()
            self.ui.passwordField.setFocus()
            self.ui.passwordField.setPlaceholderText(
                self.tr("Incorrect password. Try again.")
            )
            return
        
        logger.info(gtr("Profile selected: %s"), profile_name)
        logger.info(gtr("Decrypting profile..."))
        
        try:
            gfs = PyGocryptfs()
            gfs.mount(
                KEYS_DIR / f"{profile.uid}.conf",
                profile.cipher_path,
                profile.mount_path,
                password,
            )
            mnt = profile.mount_path
            profile.mountpoint = mnt
        except (GocryptfsNotInstalledError, MissingDependenciesError) as e:
            logger.error(
                gtr(
                    "Gocryptfs is not installed or missing dependencies. "
                    "Please install it and try again."
                )
            )
            QMessageBox.critical(
                self,
                self.tr("Fatal Error"),
                self.tr(
                    "Gocryptfs is not installed or missing dependencies. "
                    "Please install it and try again.\nDetails: {error}"
                ).format(error=str(e)),
            )
            return
        except GocryptfsError as e:
            QMessageBox.critical(
                self,
                self.tr("Fatal Error"),
                self.tr(
                    "Unable to decrypt the profile. Please check your password "
                    "and try again.\nDetails: {error}"
                ).format(error=str(e)),
            )
            return
        except Exception as e:
            logger.error(
                gtr("An unexpected error occurred while decrypting the profile: %s"),
                str(e),
            )
            QMessageBox.critical(
                self,
                self.tr("Fatal Error"),
                self.tr(
                    "An unexpected error occurred while decrypting the profile. "
                    "Please try again."
                ),
            )
            return
        
        self.profileSelected.emit(profile)
        
    def onGuestButtonClicked(self):
        self.profileSelected.emit(OtusProfile(uid="Otus Guest", name="Otus Guest"))
        
    def onCreateProfileButtonClicked(self):
        wizard = ProfileCreatorWizard(self)

        wizard.profileCreated.connect(self.onProfileCreated)
        wizard.loginRequested.connect(self.onLoginRequested)

        wizard.exec()
        
    def onProfileCreated(self, profile_id: str):
        logger.info(gtr("Profile created with ID: %s"), profile_id)
        self.refreshProfiles()

    def onLoginRequested(self, profile_id: str):
        logger.info(gtr("Login requested for profile: %s"), profile_id)
        profile = get_profile_by_id(profile_id)
        if profile is not None:
            self.profileSelected.emit(profile)