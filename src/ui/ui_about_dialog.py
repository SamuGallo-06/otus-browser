# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QSizePolicy, QWidget)
from . import resources_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(517, 408)
        self.gridLayout = QGridLayout(AboutDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.label_3 = QLabel(AboutDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setWordWrap(True)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 3)

        self.label_4 = QLabel(AboutDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 3)

        self.label_2 = QLabel(AboutDialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(128, 128))
        self.label_2.setMaximumSize(QSize(128, 128))
        self.label_2.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.label_2.setFrameShape(QFrame.Shape.WinPanel)
        self.label_2.setFrameShadow(QFrame.Shadow.Plain)
        self.label_2.setPixmap(QPixmap(u":/otus/resources/otus_logo.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(False)

        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)


        self.retranslateUi(AboutDialog)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About Otus", None))
        self.label.setText(QCoreApplication.translate("AboutDialog", u"# About Otus", None))
        self.label_3.setText(QCoreApplication.translate("AboutDialog", u"A privacy-focused web browser built with PySide6 and Qt WebEngine. <p>For more information, visit <a href='https://github.com/SamuGallo-06/otus-browser'>the project repository</a>.</p>", None))
        self.label_4.setText(QCoreApplication.translate("AboutDialog", u"<html><head/><body><p>Created by Samuele Gallicani</p></body></html>", None))
        self.label_2.setText("")
    # retranslateUi

