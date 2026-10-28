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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)
from . import resources_rc

class Ui_ProfileSelectionWidget(object):
    def setupUi(self, ProfileSelectionWidget):
        if not ProfileSelectionWidget.objectName():
            ProfileSelectionWidget.setObjectName(u"ProfileSelectionWidget")
        ProfileSelectionWidget.resize(517, 408)
        self.gridLayout = QGridLayout(ProfileSelectionWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(ProfileSelectionWidget)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.passwordField = QLineEdit(ProfileSelectionWidget)
        self.passwordField.setObjectName(u"passwordField")
        self.passwordField.setEchoMode(QLineEdit.EchoMode.Password)

        self.gridLayout.addWidget(self.passwordField, 3, 0, 1, 3)

        self.profilesComboBox = QComboBox(ProfileSelectionWidget)
        self.profilesComboBox.setObjectName(u"profilesComboBox")

        self.gridLayout.addWidget(self.profilesComboBox, 2, 0, 1, 3)

        self.loginButton = QPushButton(ProfileSelectionWidget)
        self.loginButton.setObjectName(u"loginButton")
        icon = QIcon()
        icon.addFile(u":/feather/resources/feather/log-out.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.loginButton.setIcon(icon)

        self.gridLayout.addWidget(self.loginButton, 5, 2, 1, 1)

        self.guestProfileButton = QPushButton(ProfileSelectionWidget)
        self.guestProfileButton.setObjectName(u"guestProfileButton")

        self.gridLayout.addWidget(self.guestProfileButton, 5, 0, 1, 1)

        self.label_2 = QLabel(ProfileSelectionWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(128, 128))
        self.label_2.setMaximumSize(QSize(200, 200))
        self.label_2.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.label_2.setFrameShape(QFrame.Shape.WinPanel)
        self.label_2.setFrameShadow(QFrame.Shadow.Plain)
        self.label_2.setPixmap(QPixmap(u":/otus/resources/otus_logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(False)

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)

        self.newProfileButton = QPushButton(ProfileSelectionWidget)
        self.newProfileButton.setObjectName(u"newProfileButton")
        icon1 = QIcon()
        icon1.addFile(u":/feather/resources/feather/user-plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.newProfileButton.setIcon(icon1)

        self.gridLayout.addWidget(self.newProfileButton, 5, 1, 1, 1)


        self.retranslateUi(ProfileSelectionWidget)

        QMetaObject.connectSlotsByName(ProfileSelectionWidget)
    # setupUi

    def retranslateUi(self, ProfileSelectionWidget):
        ProfileSelectionWidget.setWindowTitle(QCoreApplication.translate("ProfileSelectionWidget", u"Select Profile - Otus Browser", None))
        self.label.setText(QCoreApplication.translate("ProfileSelectionWidget", u"# Welcome to Otus Browser", None))
        self.passwordField.setInputMask("")
        self.passwordField.setPlaceholderText(QCoreApplication.translate("ProfileSelectionWidget", u"Password", None))
        self.profilesComboBox.setCurrentText("")
        self.profilesComboBox.setPlaceholderText(QCoreApplication.translate("ProfileSelectionWidget", u"No profiles available, Please create a profile first", None))
        self.loginButton.setText(QCoreApplication.translate("ProfileSelectionWidget", u"Login", None))
        self.guestProfileButton.setText(QCoreApplication.translate("ProfileSelectionWidget", u"Guest", None))
        self.label_2.setText("")
        self.newProfileButton.setText(QCoreApplication.translate("ProfileSelectionWidget", u"New Profile", None))
    # retranslateUi

