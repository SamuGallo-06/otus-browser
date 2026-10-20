# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QToolBar, QWidget)
from . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/App Icons/c2d71cbe/otus_logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionSilentwing = QAction(MainWindow)
        self.actionSilentwing.setObjectName(u"actionSilentwing")
        self.actionSilentwing.setCheckable(True)
        self.actionSilentwing.setMenuRole(QAction.MenuRole.NoRole)
        self.actionHome = QAction(MainWindow)
        self.actionHome.setObjectName(u"actionHome")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))
        self.actionHome.setIcon(icon1)
        self.actionHome.setMenuRole(QAction.MenuRole.NoRole)
        self.actionReload = QAction(MainWindow)
        self.actionReload.setObjectName(u"actionReload")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ViewRefresh))
        self.actionReload.setIcon(icon2)
        self.actionReload.setMenuRole(QAction.MenuRole.NoRole)
        self.actionForward = QAction(MainWindow)
        self.actionForward.setObjectName(u"actionForward")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoNext))
        self.actionForward.setIcon(icon3)
        self.actionForward.setMenuRole(QAction.MenuRole.NoRole)
        self.actionBack = QAction(MainWindow)
        self.actionBack.setObjectName(u"actionBack")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoPrevious))
        self.actionBack.setIcon(icon4)
        self.actionBack.setMenuRole(QAction.MenuRole.NoRole)
        self.actionNew_Tab = QAction(MainWindow)
        self.actionNew_Tab.setObjectName(u"actionNew_Tab")
        self.actionNew_Window = QAction(MainWindow)
        self.actionNew_Window.setObjectName(u"actionNew_Window")
        self.actionNew_Private_Window = QAction(MainWindow)
        self.actionNew_Private_Window.setObjectName(u"actionNew_Private_Window")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.browserTabWidget = QTabWidget(self.centralwidget)
        self.browserTabWidget.setObjectName(u"browserTabWidget")
        self.browserTabWidget.setDocumentMode(True)
        self.browserTabWidget.setTabsClosable(True)
        self.browserTabWidget.setMovable(True)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.browserTabWidget.addTab(self.tab, icon1, "")

        self.gridLayout.addWidget(self.browserTabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionNew_Tab)
        self.menuFile.addAction(self.actionNew_Window)
        self.menuFile.addAction(self.actionNew_Private_Window)
        self.toolBar.addAction(self.actionBack)
        self.toolBar.addAction(self.actionHome)
        self.toolBar.addAction(self.actionForward)
        self.toolBar.addAction(self.actionReload)
        self.toolBar.addAction(self.actionSilentwing)

        self.retranslateUi(MainWindow)

        self.browserTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Otus Browser", None))
        self.actionSilentwing.setText(QCoreApplication.translate("MainWindow", u"Silent Wing", None))
#if QT_CONFIG(shortcut)
        self.actionSilentwing.setShortcut(QCoreApplication.translate("MainWindow", u"F6", None))
#endif // QT_CONFIG(shortcut)
        self.actionHome.setText(QCoreApplication.translate("MainWindow", u"Home", None))
#if QT_CONFIG(tooltip)
        self.actionHome.setToolTip(QCoreApplication.translate("MainWindow", u"Open the home page", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionHome.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+H", None))
#endif // QT_CONFIG(shortcut)
        self.actionReload.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
#if QT_CONFIG(tooltip)
        self.actionReload.setToolTip(QCoreApplication.translate("MainWindow", u"Reload this page", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionReload.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionForward.setText(QCoreApplication.translate("MainWindow", u"Forward", None))
#if QT_CONFIG(shortcut)
        self.actionForward.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+Right", None))
#endif // QT_CONFIG(shortcut)
        self.actionBack.setText(QCoreApplication.translate("MainWindow", u"Back", None))
#if QT_CONFIG(shortcut)
        self.actionBack.setShortcut(QCoreApplication.translate("MainWindow", u"Alt+Left", None))
#endif // QT_CONFIG(shortcut)
        self.actionNew_Tab.setText(QCoreApplication.translate("MainWindow", u"New Tab", None))
        self.actionNew_Window.setText(QCoreApplication.translate("MainWindow", u"New Window", None))
        self.actionNew_Private_Window.setText(QCoreApplication.translate("MainWindow", u"New Private Window", None))
        self.browserTabWidget.setTabText(self.browserTabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Home", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

