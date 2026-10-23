# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile_creator_wizard.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QLabel,
    QLineEdit, QProgressBar, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget, QWizard, QWizardPage)

class Ui_ProfileCreatorWizard(object):
    def setupUi(self, ProfileCreatorWizard):
        if not ProfileCreatorWizard.objectName():
            ProfileCreatorWizard.setObjectName(u"ProfileCreatorWizard")
        ProfileCreatorWizard.resize(400, 300)
        ProfileCreatorWizard.setWizardStyle(QWizard.WizardStyle.ClassicStyle)
        self.welcomePage = QWizardPage()
        self.welcomePage.setObjectName(u"welcomePage")
        self.gridLayout = QGridLayout(self.welcomePage)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.welcomePage)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        ProfileCreatorWizard.setPage(0, self.welcomePage)
        self.profileNamePage = QWizardPage()
        self.profileNamePage.setObjectName(u"profileNamePage")
        self.gridLayout_2 = QGridLayout(self.profileNamePage)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.profileNamePage)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.profileNameField = QLineEdit(self.profileNamePage)
        self.profileNameField.setObjectName(u"profileNameField")

        self.gridLayout_2.addWidget(self.profileNameField, 1, 0, 1, 1)

        ProfileCreatorWizard.setPage(1, self.profileNamePage)
        self.encryptionPage = QWizardPage()
        self.encryptionPage.setObjectName(u"encryptionPage")
        self.gridLayout_3 = QGridLayout(self.encryptionPage)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.encryptionPage)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)

        self.encryptProfileCheckbox = QCheckBox(self.encryptionPage)
        self.encryptProfileCheckbox.setObjectName(u"encryptProfileCheckbox")

        self.gridLayout_3.addWidget(self.encryptProfileCheckbox, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 0, 1, 1)

        ProfileCreatorWizard.setPage(2, self.encryptionPage)
        self.passwordPage = QWizardPage()
        self.passwordPage.setObjectName(u"passwordPage")
        self.verticalLayout = QVBoxLayout(self.passwordPage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(self.passwordPage)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.passwordField = QLineEdit(self.passwordPage)
        self.passwordField.setObjectName(u"passwordField")

        self.verticalLayout.addWidget(self.passwordField)

        self.label_5 = QLabel(self.passwordPage)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.passwordCheckField = QLineEdit(self.passwordPage)
        self.passwordCheckField.setObjectName(u"passwordCheckField")

        self.verticalLayout.addWidget(self.passwordCheckField)

        ProfileCreatorWizard.setPage(3, self.passwordPage)
        self.progressPage = QWizardPage()
        self.progressPage.setObjectName(u"progressPage")
        self.gridLayout_4 = QGridLayout(self.progressPage)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.statusLabel = QLabel(self.progressPage)
        self.statusLabel.setObjectName(u"statusLabel")

        self.gridLayout_4.addWidget(self.statusLabel, 0, 0, 1, 1)

        self.progressBar = QProgressBar(self.progressPage)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(-1)

        self.gridLayout_4.addWidget(self.progressBar, 1, 0, 1, 1)

        ProfileCreatorWizard.setPage(4, self.progressPage)
        self.finishPage = QWizardPage()
        self.finishPage.setObjectName(u"finishPage")
        self.verticalLayout_2 = QVBoxLayout(self.finishPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_6 = QLabel(self.finishPage)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.loginNowCheckBox = QCheckBox(self.finishPage)
        self.loginNowCheckBox.setObjectName(u"loginNowCheckBox")

        self.verticalLayout_2.addWidget(self.loginNowCheckBox)

        ProfileCreatorWizard.setPage(5, self.finishPage)

        self.retranslateUi(ProfileCreatorWizard)

        QMetaObject.connectSlotsByName(ProfileCreatorWizard)
    # setupUi

    def retranslateUi(self, ProfileCreatorWizard):
        ProfileCreatorWizard.setWindowTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Profile Creator Wizard - Otus Browser", None))
        self.welcomePage.setTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Create a Profile", None))
        self.welcomePage.setSubTitle("")
        self.label_2.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Welcome to the Profile Creator Wizard!\n"
"\n"
"This tool will guide you step-by-step through setting up a new customized profile, ensuring maximum privacy and security for your browsing experience", None))
        self.profileNamePage.setTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Create Profile", None))
        self.profileNamePage.setSubTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Choose a Username", None))
        self.label.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Enter a name to identify this profile in the dropdown menu", None))
        self.encryptionPage.setTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Create a Profile", None))
        self.encryptionPage.setSubTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Choose a password for the profile", None))
        self.label_3.setText(QCoreApplication.translate("ProfileCreatorWizard", u"To keep your data private, you can protect this profile with a password.\n"
"Enabling encryption ensures that your settings and browsing data are securely locked when you log out.", None))
        self.encryptProfileCheckbox.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Encrypt this profile", None))
        self.passwordPage.setTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Create a Profile", None))
        self.passwordPage.setSubTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Choose a password for the profile", None))
        self.label_4.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Password", None))
        self.label_5.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Password Confirmation", None))
        self.progressPage.setTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Create a Profile", None))
        self.progressPage.setSubTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Working on it...", None))
        self.statusLabel.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Creating profile...", None))
        self.finishPage.setTitle(QCoreApplication.translate("ProfileCreatorWizard", u"Profile Created!", None))
        self.finishPage.setSubTitle(QCoreApplication.translate("ProfileCreatorWizard", u"You're all set!", None))
        self.label_6.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Your new profile is ready to use. You can now select it from the dropdown menu and switch between profiles at any time, or log in right now.", None))
        self.loginNowCheckBox.setText(QCoreApplication.translate("ProfileCreatorWizard", u"Log in with your profile", None))
    # retranslateUi

