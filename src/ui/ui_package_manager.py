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
from PySide6.QtWidgets import (QApplication, QDockWidget, QGridLayout, QLineEdit,
    QListView, QListWidget, QListWidgetItem, QPlainTextEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

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
        self.detailsLayout = QVBoxLayout(self.dockWidgetContents)
        self.detailsLayout.setObjectName(u"detailsLayout")
        self.detailsText = QPlainTextEdit(self.dockWidgetContents)
        self.detailsText.setObjectName(u"detailsText")
        self.detailsText.setReadOnly(True)

        self.detailsLayout.addWidget(self.detailsText)

        self.uninstallPackageButton = QPushButton(self.dockWidgetContents)
        self.uninstallPackageButton.setObjectName(u"uninstallPackageButton")
        self.uninstallPackageButton.setEnabled(False)

        self.detailsLayout.addWidget(self.uninstallPackageButton)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.gridLayout_2.addWidget(self.dockWidget, 2, 0, 1, 1)

        self.installPackageButton = QPushButton(OtusPackageManager)
        self.installPackageButton.setObjectName(u"installPackageButton")

        self.gridLayout_2.addWidget(self.installPackageButton, 3, 0, 1, 1)

        self.packageList = QListWidget(OtusPackageManager)
        self.packageList.setObjectName(u"packageList")
        self.packageList.setViewMode(QListView.IconMode)
        self.packageList.setIconSize(QSize(64, 64))
        self.packageList.setResizeMode(QListView.Adjust)
        self.packageList.setMovement(QListView.Static)
        self.packageList.setSpacing(12)
        self.packageList.setUniformItemSizes(True)

        self.gridLayout_2.addWidget(self.packageList, 1, 0, 1, 1)

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
        self.uninstallPackageButton.setText(QCoreApplication.translate("OtusPackageManager", u"Uninstall", None))
        self.installPackageButton.setText(QCoreApplication.translate("OtusPackageManager", u"Install Package", None))
        self.searchBox.setPlaceholderText(QCoreApplication.translate("OtusPackageManager", u"Search Packages...", None))
    # retranslateUi

