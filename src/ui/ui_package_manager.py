# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_manager.ui'
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
from PySide6.QtWidgets import (QApplication, QDockWidget, QGridLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QWidget)

class Ui_OtusPackageManager(object):
    def setupUi(self, OtusPackageManager):
        if not OtusPackageManager.objectName():
            OtusPackageManager.setObjectName(u"OtusPackageManager")
        OtusPackageManager.resize(600, 534)
        self.gridLayout_2 = QGridLayout(OtusPackageManager)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.dockWidget = QDockWidget(OtusPackageManager)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidget.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea|Qt.DockWidgetArea.LeftDockWidgetArea|Qt.DockWidgetArea.RightDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout = QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.dockWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.dockWidgetContents)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_3 = QLabel(self.dockWidgetContents)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.gridLayout_2.addWidget(self.dockWidget, 2, 0, 1, 1)

        self.installPackageButton = QPushButton(OtusPackageManager)
        self.installPackageButton.setObjectName(u"installPackageButton")

        self.gridLayout_2.addWidget(self.installPackageButton, 3, 0, 1, 1)

        self.scrollArea = QScrollArea(OtusPackageManager)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 580, 221))
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.searchBox = QLineEdit(OtusPackageManager)
        self.searchBox.setObjectName(u"searchBox")
        self.searchBox.setClearButtonEnabled(True)

        self.gridLayout_2.addWidget(self.searchBox, 0, 0, 1, 1)


        self.retranslateUi(OtusPackageManager)

        QMetaObject.connectSlotsByName(OtusPackageManager)
    # setupUi

    def retranslateUi(self, OtusPackageManager):
        OtusPackageManager.setWindowTitle(QCoreApplication.translate("OtusPackageManager", u"Package Manager - Otus Browser", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("OtusPackageManager", u"Details", None))
        self.label_2.setText(QCoreApplication.translate("OtusPackageManager", u"Version", None))
        self.label.setText(QCoreApplication.translate("OtusPackageManager", u"Description: ", None))
        self.label_3.setText(QCoreApplication.translate("OtusPackageManager", u"Authors", None))
        self.installPackageButton.setText(QCoreApplication.translate("OtusPackageManager", u"Install Package", None))
        self.searchBox.setPlaceholderText(QCoreApplication.translate("OtusPackageManager", u"Search Packages...", None))
    # retranslateUi

