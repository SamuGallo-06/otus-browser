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
from PySide6.QtWidgets import (QApplication, QScrollArea, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_BookmarksForm(object):
    def setupUi(self, BookmarksForm):
        if not BookmarksForm.objectName():
            BookmarksForm.setObjectName(u"BookmarksForm")
        BookmarksForm.resize(400, 300)
        self.verticalLayout = QVBoxLayout(BookmarksForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(BookmarksForm)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 380, 280))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(BookmarksForm)

        QMetaObject.connectSlotsByName(BookmarksForm)
    # setupUi

    def retranslateUi(self, BookmarksForm):
        BookmarksForm.setWindowTitle(QCoreApplication.translate("BookmarksForm", u"Bookmarks - Otus Browser", None))
    # retranslateUi

