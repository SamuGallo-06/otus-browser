# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bookmarks.ui'
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
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_BookmarksLibrary(object):
    def setupUi(self, BookmarksLibrary):
        if not BookmarksLibrary.objectName():
            BookmarksLibrary.setObjectName(u"BookmarksLibrary")
        BookmarksLibrary.resize(522, 444)
        self.gridLayout = QGridLayout(BookmarksLibrary)
        self.gridLayout.setObjectName(u"gridLayout")
        self.exportButton = QPushButton(BookmarksLibrary)
        self.exportButton.setObjectName(u"exportButton")

        self.gridLayout.addWidget(self.exportButton, 2, 2, 1, 1)

        self.importButton = QPushButton(BookmarksLibrary)
        self.importButton.setObjectName(u"importButton")

        self.gridLayout.addWidget(self.importButton, 2, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.scrollArea = QScrollArea(BookmarksLibrary)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 502, 360))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)

        self.searchBox = QLineEdit(BookmarksLibrary)
        self.searchBox.setObjectName(u"searchBox")

        self.gridLayout.addWidget(self.searchBox, 0, 0, 1, 3)


        self.retranslateUi(BookmarksLibrary)

        QMetaObject.connectSlotsByName(BookmarksLibrary)
    # setupUi

    def retranslateUi(self, BookmarksLibrary):
        BookmarksLibrary.setWindowTitle(QCoreApplication.translate("BookmarksLibrary", u"Bookmarks - Otus Browser", None))
        self.exportButton.setText(QCoreApplication.translate("BookmarksLibrary", u"Export Bookmarks", None))
        self.importButton.setText(QCoreApplication.translate("BookmarksLibrary", u"Import Bookmarks", None))
        self.label.setText(QCoreApplication.translate("BookmarksLibrary", u"TextLabel", None))
        self.searchBox.setPlaceholderText(QCoreApplication.translate("BookmarksLibrary", u"Search Bookmarks", None))
    # retranslateUi

