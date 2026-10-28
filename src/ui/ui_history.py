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
from PySide6.QtWidgets import (QApplication, QDateEdit, QGridLayout, QHeaderView,
    QLineEdit, QPushButton, QScrollArea, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
from . import resources_rc

class Ui_HistoryForm(object):
    def setupUi(self, HistoryForm):
        if not HistoryForm.objectName():
            HistoryForm.setObjectName(u"HistoryForm")
        HistoryForm.resize(737, 584)
        self.verticalLayout = QVBoxLayout(HistoryForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea = QScrollArea(HistoryForm)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 717, 564))
        self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.historyTable = QTableWidget(self.scrollAreaWidgetContents)
        if (self.historyTable.columnCount() < 5):
            self.historyTable.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.historyTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.historyTable.setObjectName(u"historyTable")
        self.historyTable.setGridStyle(Qt.PenStyle.NoPen)
        self.historyTable.setSortingEnabled(False)

        self.gridLayout.addWidget(self.historyTable, 1, 0, 1, 3)

        self.deleteSince = QPushButton(self.scrollAreaWidgetContents)
        self.deleteSince.setObjectName(u"deleteSince")
        icon = QIcon()
        icon.addFile(u":/feather/resources/feather/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deleteSince.setIcon(icon)

        self.gridLayout.addWidget(self.deleteSince, 3, 1, 1, 1)

        self.dateEdit = QDateEdit(self.scrollAreaWidgetContents)
        self.dateEdit.setObjectName(u"dateEdit")

        self.gridLayout.addWidget(self.dateEdit, 3, 2, 1, 1)

        self.deleteAllButton = QPushButton(self.scrollAreaWidgetContents)
        self.deleteAllButton.setObjectName(u"deleteAllButton")
        self.deleteAllButton.setIcon(icon)

        self.gridLayout.addWidget(self.deleteAllButton, 3, 0, 1, 1)

        self.searchBox = QLineEdit(self.scrollAreaWidgetContents)
        self.searchBox.setObjectName(u"searchBox")

        self.gridLayout.addWidget(self.searchBox, 0, 0, 1, 3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(HistoryForm)

        QMetaObject.connectSlotsByName(HistoryForm)
    # setupUi

    def retranslateUi(self, HistoryForm):
        HistoryForm.setWindowTitle(QCoreApplication.translate("HistoryForm", u"History - Otus Browser", None))
        ___qtablewidgetitem = self.historyTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("HistoryForm", u"URL", None))
        ___qtablewidgetitem1 = self.historyTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("HistoryForm", u"Title", None))
        ___qtablewidgetitem2 = self.historyTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("HistoryForm", u"Visited At", None))
        ___qtablewidgetitem3 = self.historyTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("HistoryForm", u"Count", None))
        self.deleteSince.setText(QCoreApplication.translate("HistoryForm", u"Delete history since", None))
        self.deleteAllButton.setText(QCoreApplication.translate("HistoryForm", u"Delete history", None))
        self.searchBox.setPlaceholderText(QCoreApplication.translate("HistoryForm", u"Search History...", None))
    # retranslateUi

