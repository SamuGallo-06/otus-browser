# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'history.ui'
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

class Ui_HistoryForm(object):
    def setupUi(self, HistoryForm):
        if not HistoryForm.objectName():
            HistoryForm.setObjectName(u"HistoryForm")
        HistoryForm.resize(400, 300)
        self.verticalLayout = QVBoxLayout(HistoryForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(HistoryForm)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 380, 280))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(HistoryForm)

        QMetaObject.connectSlotsByName(HistoryForm)
    # setupUi

    def retranslateUi(self, HistoryForm):
        HistoryForm.setWindowTitle(QCoreApplication.translate("HistoryForm", u"History - Otus Browser", None))
    # retranslateUi

