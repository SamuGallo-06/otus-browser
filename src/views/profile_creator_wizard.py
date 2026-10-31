from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QLineEdit, QMessageBox, QWizard

from ui.ui_profile_creator_wizard import Ui_ProfileCreatorWizard
from profiles import createProfile

(PAGE_WELCOME, PAGE_NAME, PAGE_ENCRYPTION,
 PAGE_PASSWORD, PAGE_PROGRESS, PAGE_FINISH) = range(6)

MIN_PASSWORD_LENGTH = 8

class ProfileCreatorWizard(QWizard):
    profileCreated = Signal(str)
    loginRequested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ProfileCreatorWizard()
        self.ui.setupUi(self)
        self._busy = False
        self._created_profile_id: str | None = None

        # At the last page, the Back button is disabled (at this time, the profile already exists).
        self.setOption(QWizard.WizardOption.DisabledBackButtonOnLastPage, True)

        # Le password non devono essere visibili mentre si scrivono
        self.ui.passwordField.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.passwordCheckField.setEchoMode(QLineEdit.EchoMode.Password)

        self.currentIdChanged.connect(self.onPageChanged)

    # ------------------------------------------------------------------
    # Navigazione
    # ------------------------------------------------------------------
    def nextId(self) -> int:
        """Dalla pagina di cifratura si salta la password se la casella non è spuntata.
        Il tasto Back segue da solo la cronologia delle pagine visitate."""
        if self.currentId() == PAGE_ENCRYPTION:
            if self.ui.encryptProfileCheckbox.isChecked():
                return PAGE_PASSWORD
            return PAGE_PROGRESS
        return super().nextId()

    def validateCurrentPage(self) -> bool:
        """Chiamata quando si preme Next/Finish: False blocca il passaggio."""
        page = self.currentId()

        if page == PAGE_NAME:
            if not self.profileName():
                return self._warn(self.tr("Enter a name for the profile."))
            # TODO: controlla che non esista già un profilo con questo nome

        elif page == PAGE_PASSWORD:
            password = self.ui.passwordField.text()
            if len(password) < MIN_PASSWORD_LENGTH:
                return self._warn(
                    self.tr(
                        "The password must be at least {length} characters long."
                    ).format(length=MIN_PASSWORD_LENGTH)
                )
            if password != self.ui.passwordCheckField.text():
                return self._warn(self.tr("The two passwords do not match."))

        return True

    def onPageChanged(self, page_id: int):
        if page_id == PAGE_PASSWORD:
            self.ui.passwordField.setFocus()
        elif page_id == PAGE_PROGRESS:
            QTimer.singleShot(0, self._startCreation)

    # ------------------------------------------------------------------
    # Creazione del profilo (pagina di avanzamento)
    # ------------------------------------------------------------------
    def _startCreation(self):
        self._busy = True
        self._setNavigationEnabled(False)

        name = self.profileName()
        password = (self.ui.passwordField.text()
                    if self.ui.encryptProfileCheckbox.isChecked() else None)

        try:
            self._created_profile_id = createProfile(name, password)
        except Exception as error:
            self.creationFailed(str(error))
            return

        self.creationDone()

    def creationDone(self):
        self._busy = False
        self._setNavigationEnabled(True)
        if self._created_profile_id is None:
            self.creationFailed(self.tr("The profile ID was not generated."))
            return

        self.profileCreated.emit(self._created_profile_id)
        self.next()

    def creationFailed(self, message: str):
        self._busy = False
        self._setNavigationEnabled(True)
        self._warn(self.tr("The profile could not be created.\n\n{message}").format(
            message=message
        ))
        self.back()

    # ------------------------------------------------------------------
    # Chiusura
    # ------------------------------------------------------------------
    def accept(self):
        super().accept()
        if self.ui.loginNowCheckBox.isChecked() and self._created_profile_id is not None:
            self.loginRequested.emit(self._created_profile_id)

    def reject(self):
        if self._busy:
            return
        super().reject()

    def done(self, result: int):
        self.ui.passwordField.clear()
        self.ui.passwordCheckField.clear()
        super().done(result)

    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    def profileName(self) -> str:
        return self.ui.profileNameField.text().strip()

    def _warn(self, text: str) -> bool:
        QMessageBox.warning(self, self.tr("Profile Creator"), text)
        return False

    def _setNavigationEnabled(self, enabled: bool):
        for which in (QWizard.WizardButton.BackButton,
                      QWizard.WizardButton.NextButton,
                      QWizard.WizardButton.CancelButton):
            button = self.button(which)
            if button is not None:
                button.setEnabled(enabled)