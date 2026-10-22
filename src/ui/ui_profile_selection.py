# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'profile_selection.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_ProfileSelectionWidget(object):
    def setupUi(self, ProfileSelectionWidget):
        if not ProfileSelectionWidget.objectName():
            ProfileSelectionWidget.setObjectName(u"ProfileSelectionWidget")
        ProfileSelectionWidget.resize(400, 300)
        self.gridLayout = QGridLayout(ProfileSelectionWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.newProfileButton = QPushButton(ProfileSelectionWidget)
        self.newProfileButton.setObjectName(u"newProfileButton")

        self.gridLayout.addWidget(self.newProfileButton, 5, 1, 1, 1)

        self.loginButton = QPushButton(ProfileSelectionWidget)
        self.loginButton.setObjectName(u"loginButton")

        self.gridLayout.addWidget(self.loginButton, 5, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.profilesComboBox = QComboBox(ProfileSelectionWidget)
        self.profilesComboBox.setObjectName(u"profilesComboBox")

        self.gridLayout.addWidget(self.profilesComboBox, 2, 0, 1, 3)

        self.label = QLabel(ProfileSelectionWidget)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.passwordField = QLineEdit(ProfileSelectionWidget)
        self.passwordField.setObjectName(u"passwordField")
        self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.passwordField, 3, 0, 1, 3)

        self.guestProfileButton = QPushButton(ProfileSelectionWidget)
        self.guestProfileButton.setObjectName(u"guestProfileButton")

        self.gridLayout.addWidget(self.guestProfileButton, 5, 0, 1, 1)

        self.usersIcon = QLabel(ProfileSelectionWidget)
        self.usersIcon.setObjectName(u"usersIcon")
        self.usersIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.usersIcon, 1, 0, 1, 3)


        self.retranslateUi(ProfileSelectionWidget)

        QMetaObject.connectSlotsByName(ProfileSelectionWidget)
    # setupUi

    def retranslateUi(self, ProfileSelectionWidget):
        ProfileSelectionWidget.setWindowTitle(QCoreApplication.translate("ProfileSelectionWidget", u"Select Profile - Otus Browser", None))
        self.newProfileButton.setText(QCoreApplication.translate("ProfileSelectionWidget", u"New Profile", None))
        self.loginButton.setText(QCoreApplication.translate("ProfileSelectionWidget", u"Login", None))
        self.profilesComboBox.setCurrentText("")
        self.profilesComboBox.setPlaceholderText(QCoreApplication.translate("ProfileSelectionWidget", u"No profiles available, Please create a profile first", None))
        self.label.setText(QCoreApplication.translate("ProfileSelectionWidget", u"# Welcome to Otus Browser", None))
        self.passwordField.setInputMask("")
        self.passwordField.setPlaceholderText(QCoreApplication.translate("ProfileSelectionWidget", u"Password", None))
        self.guestProfileButton.setText(QCoreApplication.translate("ProfileSelectionWidget", u"Guest", None))
        self.usersIcon.setText(QCoreApplication.translate("ProfileSelectionWidget", u"TextLabel", None))
    # retranslateUi

