# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_bookmark.ui'
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
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_EditBookmarkDialog(object):
    def setupUi(self, EditBookmarkDialog):
        if not EditBookmarkDialog.objectName():
            EditBookmarkDialog.setObjectName(u"EditBookmarkDialog")
        EditBookmarkDialog.setWindowModality(Qt.WindowModality.WindowModal)
        EditBookmarkDialog.resize(400, 256)
        self.gridLayout = QGridLayout(EditBookmarkDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.titleField = QLineEdit(EditBookmarkDialog)
        self.titleField.setObjectName(u"titleField")

        self.gridLayout.addWidget(self.titleField, 1, 0, 1, 3)

        self.descriptionField = QLineEdit(EditBookmarkDialog)
        self.descriptionField.setObjectName(u"descriptionField")

        self.gridLayout.addWidget(self.descriptionField, 3, 0, 1, 3)

        self.label_2 = QLabel(EditBookmarkDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)

        self.saveButton = QPushButton(EditBookmarkDialog)
        self.saveButton.setObjectName(u"saveButton")

        self.gridLayout.addWidget(self.saveButton, 7, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 1, 1, 1)

        self.urlField = QLineEdit(EditBookmarkDialog)
        self.urlField.setObjectName(u"urlField")

        self.gridLayout.addWidget(self.urlField, 5, 0, 1, 3)

        self.label_3 = QLabel(EditBookmarkDialog)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 2)

        self.label = QLabel(EditBookmarkDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.cancelButton = QPushButton(EditBookmarkDialog)
        self.cancelButton.setObjectName(u"cancelButton")

        self.gridLayout.addWidget(self.cancelButton, 7, 1, 1, 1)


        self.retranslateUi(EditBookmarkDialog)

        QMetaObject.connectSlotsByName(EditBookmarkDialog)
    # setupUi

    def retranslateUi(self, EditBookmarkDialog):
        EditBookmarkDialog.setWindowTitle(QCoreApplication.translate("EditBookmarkDialog", u"Edit Bookmark", None))
        self.label_2.setText(QCoreApplication.translate("EditBookmarkDialog", u"Description", None))
        self.saveButton.setText(QCoreApplication.translate("EditBookmarkDialog", u"Save", None))
        self.label_3.setText(QCoreApplication.translate("EditBookmarkDialog", u"URL", None))
        self.label.setText(QCoreApplication.translate("EditBookmarkDialog", u"Title", None))
        self.cancelButton.setText(QCoreApplication.translate("EditBookmarkDialog", u"Cancel", None))
    # retranslateUi

