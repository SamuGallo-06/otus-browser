# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download_manager.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_DownloadHistory(object):
    def setupUi(self, DownloadHistory):
        if not DownloadHistory.objectName():
            DownloadHistory.setObjectName(u"DownloadHistory")
        DownloadHistory.resize(397, 289)
        self.gridLayout = QGridLayout(DownloadHistory)
        self.gridLayout.setObjectName(u"gridLayout")
        self.searchBox = QLineEdit(DownloadHistory)
        self.searchBox.setObjectName(u"searchBox")
        self.searchBox.setFrame(True)
        self.searchBox.setClearButtonEnabled(True)

        self.gridLayout.addWidget(self.searchBox, 0, 1, 1, 1)

        self.clearHistoryButton = QPushButton(DownloadHistory)
        self.clearHistoryButton.setObjectName(u"clearHistoryButton")

        self.gridLayout.addWidget(self.clearHistoryButton, 0, 0, 1, 1)

        self.scrollArea = QScrollArea(DownloadHistory)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 377, 237))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 2)


        self.retranslateUi(DownloadHistory)

        QMetaObject.connectSlotsByName(DownloadHistory)
    # setupUi

    def retranslateUi(self, DownloadHistory):
        DownloadHistory.setWindowTitle(QCoreApplication.translate("DownloadHistory", u"Downloads - Otus Browser", None))
        self.searchBox.setText("")
        self.searchBox.setPlaceholderText(QCoreApplication.translate("DownloadHistory", u"Search downloads", None))
        self.clearHistoryButton.setText(QCoreApplication.translate("DownloadHistory", u"Clear History", None))
        self.label.setText(QCoreApplication.translate("DownloadHistory", u"Recent Downloads", None))
    # retranslateUi

