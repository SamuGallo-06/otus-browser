# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'download.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)
from . import resources_rc

class Ui_DownloadWidget(object):
    def setupUi(self, DownloadWidget):
        if not DownloadWidget.objectName():
            DownloadWidget.setObjectName(u"DownloadWidget")
        DownloadWidget.resize(562, 222)
        self.gridLayout = QGridLayout(DownloadWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

        self.headerLabel = QLabel(DownloadWidget)
        self.headerLabel.setObjectName(u"headerLabel")

        self.gridLayout.addWidget(self.headerLabel, 1, 0, 1, 3)

        self.progressBar = QProgressBar(DownloadWidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.gridLayout.addWidget(self.progressBar, 2, 0, 1, 3)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)

        self.cancelDownloadButton = QPushButton(DownloadWidget)
        self.cancelDownloadButton.setObjectName(u"cancelDownloadButton")

        self.gridLayout.addWidget(self.cancelDownloadButton, 6, 0, 1, 1)

        self.openDownloadFolderButton = QPushButton(DownloadWidget)
        self.openDownloadFolderButton.setObjectName(u"openDownloadFolderButton")

        self.gridLayout.addWidget(self.openDownloadFolderButton, 6, 2, 1, 1)

        self.pauseDownloadButton = QPushButton(DownloadWidget)
        self.pauseDownloadButton.setObjectName(u"pauseDownloadButton")

        self.gridLayout.addWidget(self.pauseDownloadButton, 6, 1, 1, 1)

        self.detailsLabel = QLabel(DownloadWidget)
        self.detailsLabel.setObjectName(u"detailsLabel")

        self.gridLayout.addWidget(self.detailsLabel, 4, 0, 1, 3)

        self.label = QLabel(DownloadWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)


        self.retranslateUi(DownloadWidget)

        QMetaObject.connectSlotsByName(DownloadWidget)
    # setupUi

    def retranslateUi(self, DownloadWidget):
        DownloadWidget.setWindowTitle(QCoreApplication.translate("DownloadWidget", u"Download in progress", None))
        self.headerLabel.setText(QCoreApplication.translate("DownloadWidget", u"Downloading {filename} from {url}", None))
        self.cancelDownloadButton.setText(QCoreApplication.translate("DownloadWidget", u"Cancel", None))
        self.openDownloadFolderButton.setText(QCoreApplication.translate("DownloadWidget", u"Open Download Folder", None))
        self.pauseDownloadButton.setText(QCoreApplication.translate("DownloadWidget", u"Pause", None))
        self.detailsLabel.setText(QCoreApplication.translate("DownloadWidget", u"Downloaded {received} / {total} KB\n"
"Transfer rate: {tranfer_rate} {tr_unit} / s\n"
"Estimated time left: {eta}", None))
        self.label.setText(QCoreApplication.translate("DownloadWidget", u"<html><head/><body><p><img src=\":/feather/resources/feather/download-cloud.svg\"/></p></body></html>", None))
    # retranslateUi

