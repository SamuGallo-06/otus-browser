# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTextEdit, QToolBox,
    QWidget)
from . import resources_rc

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        if not Preferences.objectName():
            Preferences.setObjectName(u"Preferences")
        Preferences.resize(589, 528)
        icon = QIcon()
        icon.addFile(u":/feather/resources/feather/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Preferences.setWindowIcon(icon)
        self.gridLayout = QGridLayout(Preferences)
        self.gridLayout.setObjectName(u"gridLayout")
        self.restoreDefaultsButton = QPushButton(Preferences)
        self.restoreDefaultsButton.setObjectName(u"restoreDefaultsButton")
        icon1 = QIcon()
        icon1.addFile(u":/feather/resources/feather/delete.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.restoreDefaultsButton.setIcon(icon1)

        self.gridLayout.addWidget(self.restoreDefaultsButton, 3, 1, 1, 1)

        self.applyButton = QPushButton(Preferences)
        self.applyButton.setObjectName(u"applyButton")
        icon2 = QIcon()
        icon2.addFile(u":/feather/resources/feather/check.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.applyButton.setIcon(icon2)
        self.applyButton.setFlat(False)

        self.gridLayout.addWidget(self.applyButton, 3, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.cancelButton = QPushButton(Preferences)
        self.cancelButton.setObjectName(u"cancelButton")
        icon3 = QIcon()
        icon3.addFile(u":/feather/resources/feather/x.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.cancelButton.setIcon(icon3)

        self.gridLayout.addWidget(self.cancelButton, 3, 2, 1, 1)

        self.toolBox = QToolBox(Preferences)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setFrameShape(QFrame.Shape.NoFrame)
        self.generals = QWidget()
        self.generals.setObjectName(u"generals")
        self.generals.setGeometry(QRect(0, 0, 571, 328))
        self.gridLayout_3 = QGridLayout(self.generals)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_7 = QLabel(self.generals)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 6, 0, 1, 1)

        self.profilesComboBox = QComboBox(self.generals)
        self.profilesComboBox.setObjectName(u"profilesComboBox")

        self.gridLayout_3.addWidget(self.profilesComboBox, 7, 3, 1, 1)

        self.askForProfileChooseCheckbox = QCheckBox(self.generals)
        self.askForProfileChooseCheckbox.setObjectName(u"askForProfileChooseCheckbox")

        self.gridLayout_3.addWidget(self.askForProfileChooseCheckbox, 9, 0, 1, 4)

        self.alwaysAskBeforeExitCheckbox = QCheckBox(self.generals)
        self.alwaysAskBeforeExitCheckbox.setObjectName(u"alwaysAskBeforeExitCheckbox")

        self.gridLayout_3.addWidget(self.alwaysAskBeforeExitCheckbox, 8, 0, 1, 4)

        self.label_8 = QLabel(self.generals)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setTextFormat(Qt.TextFormat.MarkdownText)

        self.gridLayout_3.addWidget(self.label_8, 0, 0, 1, 4)

        self.languageComboBox = QComboBox(self.generals)
        self.languageComboBox.addItem("")
        self.languageComboBox.addItem("")
        self.languageComboBox.setObjectName(u"languageComboBox")

        self.gridLayout_3.addWidget(self.languageComboBox, 1, 3, 1, 1)

        self.label_5 = QLabel(self.generals)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_3.addWidget(self.label_5, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 10, 0, 1, 1)

        self.homePageUrlField = QLineEdit(self.generals)
        self.homePageUrlField.setObjectName(u"homePageUrlField")

        self.gridLayout_3.addWidget(self.homePageUrlField, 6, 3, 1, 1)

        self.label = QLabel(self.generals)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 7, 0, 1, 1)

        self.label_6 = QLabel(self.generals)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setTextFormat(Qt.TextFormat.MarkdownText)

        self.gridLayout_3.addWidget(self.label_6, 5, 0, 1, 4)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 4, 0, 1, 1)

        self.toolBox.addItem(self.generals, u"Generals")
        self.search = QWidget()
        self.search.setObjectName(u"search")
        self.search.setGeometry(QRect(0, 0, 228, 260))
        self.gridLayout_2 = QGridLayout(self.search)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.customSearchEngineField = QLineEdit(self.search)
        self.customSearchEngineField.setObjectName(u"customSearchEngineField")

        self.gridLayout_2.addWidget(self.customSearchEngineField, 5, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 6, 1, 1, 1)

        self.label_2 = QLabel(self.search)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setTextFormat(Qt.TextFormat.MarkdownText)

        self.gridLayout_2.addWidget(self.label_2, 1, 1, 1, 1)

        self.searchEngineComboBox = QComboBox(self.search)
        self.searchEngineComboBox.addItem("")
        self.searchEngineComboBox.addItem("")
        self.searchEngineComboBox.addItem("")
        self.searchEngineComboBox.addItem("")
        self.searchEngineComboBox.addItem("")
        self.searchEngineComboBox.addItem("")
        self.searchEngineComboBox.setObjectName(u"searchEngineComboBox")

        self.gridLayout_2.addWidget(self.searchEngineComboBox, 4, 1, 1, 2)

        self.label_3 = QLabel(self.search)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setTextFormat(Qt.TextFormat.MarkdownText)
        self.label_3.setWordWrap(True)

        self.gridLayout_2.addWidget(self.label_3, 2, 1, 1, 2)

        self.useCustomSearchEngine = QCheckBox(self.search)
        self.useCustomSearchEngine.setObjectName(u"useCustomSearchEngine")

        self.gridLayout_2.addWidget(self.useCustomSearchEngine, 5, 1, 1, 1)

        self.toolBox.addItem(self.search, u"Search")
        self.appearance = QWidget()
        self.appearance.setObjectName(u"appearance")
        self.appearance.setGeometry(QRect(0, 0, 245, 178))
        self.gridLayout_4 = QGridLayout(self.appearance)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.timeFormatComboBox = QComboBox(self.appearance)
        self.timeFormatComboBox.addItem("")
        self.timeFormatComboBox.setObjectName(u"timeFormatComboBox")

        self.gridLayout_4.addWidget(self.timeFormatComboBox, 5, 1, 1, 3)

        self.dateFormatComboBox = QComboBox(self.appearance)
        self.dateFormatComboBox.addItem("")
        self.dateFormatComboBox.addItem("")
        self.dateFormatComboBox.addItem("")
        self.dateFormatComboBox.setObjectName(u"dateFormatComboBox")

        self.gridLayout_4.addWidget(self.dateFormatComboBox, 4, 1, 1, 3)

        self.label_10 = QLabel(self.appearance)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_4.addWidget(self.label_10, 5, 0, 1, 1)

        self.themesComboBox = QComboBox(self.appearance)
        self.themesComboBox.addItem("")
        self.themesComboBox.addItem("")
        self.themesComboBox.addItem("")
        self.themesComboBox.setObjectName(u"themesComboBox")

        self.gridLayout_4.addWidget(self.themesComboBox, 1, 1, 1, 3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 6, 1, 1, 1)

        self.label_12 = QLabel(self.appearance)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setTextFormat(Qt.TextFormat.MarkdownText)

        self.gridLayout_4.addWidget(self.label_12, 0, 0, 1, 1)

        self.label_9 = QLabel(self.appearance)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_4.addWidget(self.label_9, 4, 0, 1, 1)

        self.label_11 = QLabel(self.appearance)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setTextFormat(Qt.TextFormat.MarkdownText)

        self.gridLayout_4.addWidget(self.label_11, 3, 0, 1, 1)

        self.label_4 = QLabel(self.appearance)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setTextFormat(Qt.TextFormat.MarkdownText)

        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.verticalSpacer_5, 2, 1, 1, 1)

        self.toolBox.addItem(self.appearance, u"Appearance")
        self.downloads = QWidget()
        self.downloads.setObjectName(u"downloads")
        self.downloads.setGeometry(QRect(0, 0, 299, 79))
        self.gridLayout_5 = QGridLayout(self.downloads)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.label_13 = QLabel(self.downloads)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout_5.addWidget(self.label_13, 1, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_5.addItem(self.verticalSpacer_6, 3, 0, 1, 1)

        self.downloadPathField = QLineEdit(self.downloads)
        self.downloadPathField.setObjectName(u"downloadPathField")

        self.gridLayout_5.addWidget(self.downloadPathField, 1, 2, 1, 1)

        self.alwaysAskForDownloadPathCheckbox = QCheckBox(self.downloads)
        self.alwaysAskForDownloadPathCheckbox.setObjectName(u"alwaysAskForDownloadPathCheckbox")

        self.gridLayout_5.addWidget(self.alwaysAskForDownloadPathCheckbox, 2, 0, 1, 3)

        self.toolBox.addItem(self.downloads, u"Downloads")
        self.privacy_ad_blocker = QWidget()
        self.privacy_ad_blocker.setObjectName(u"privacy_ad_blocker")
        self.privacy_ad_blocker.setGeometry(QRect(0, 0, 571, 328))
        self.gridLayout_6 = QGridLayout(self.privacy_ad_blocker)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.enableAdBlockerCheckbox = QCheckBox(self.privacy_ad_blocker)
        self.enableAdBlockerCheckbox.setObjectName(u"enableAdBlockerCheckbox")

        self.gridLayout_6.addWidget(self.enableAdBlockerCheckbox, 0, 0, 1, 1)

        self.label_14 = QLabel(self.privacy_ad_blocker)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_6.addWidget(self.label_14, 1, 0, 1, 1)

        self.blockedHostsEntry = QTextEdit(self.privacy_ad_blocker)
        self.blockedHostsEntry.setObjectName(u"blockedHostsEntry")

        self.gridLayout_6.addWidget(self.blockedHostsEntry, 2, 0, 1, 1)

        self.toolBox.addItem(self.privacy_ad_blocker, u"Privacy and Ad Blocker")

        self.gridLayout.addWidget(self.toolBox, 2, 0, 1, 4)


        self.retranslateUi(Preferences)

        self.applyButton.setDefault(True)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(4)


        QMetaObject.connectSlotsByName(Preferences)
    # setupUi

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(QCoreApplication.translate("Preferences", u"Preferences - Otus Browser", None))
        self.restoreDefaultsButton.setText(QCoreApplication.translate("Preferences", u"Restore Defaults", None))
        self.applyButton.setText(QCoreApplication.translate("Preferences", u"Apply", None))
        self.cancelButton.setText(QCoreApplication.translate("Preferences", u"Cancel", None))
        self.label_7.setText(QCoreApplication.translate("Preferences", u"Home Page URL", None))
        self.askForProfileChooseCheckbox.setText(QCoreApplication.translate("Preferences", u"Ask for Profile choose at startup", None))
        self.alwaysAskBeforeExitCheckbox.setText(QCoreApplication.translate("Preferences", u"Always ask before exiting the browser", None))
        self.label_8.setText(QCoreApplication.translate("Preferences", u"**System**", None))
        self.languageComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"English", None))
        self.languageComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"Italian", None))

        self.label_5.setText(QCoreApplication.translate("Preferences", u"Language", None))
        self.label.setText(QCoreApplication.translate("Preferences", u"Default Profile", None))
        self.label_6.setText(QCoreApplication.translate("Preferences", u"**Home Page and Startup**", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.generals), QCoreApplication.translate("Preferences", u"Generals", None))
        self.label_2.setText(QCoreApplication.translate("Preferences", u"**Search Engine**", None))
        self.searchEngineComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"DuckDuckGo (Suggested)", None))
        self.searchEngineComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"Brave Search", None))
        self.searchEngineComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"Qwant", None))
        self.searchEngineComboBox.setItemText(3, QCoreApplication.translate("Preferences", u"Startpage", None))
        self.searchEngineComboBox.setItemText(4, QCoreApplication.translate("Preferences", u"Google", None))
        self.searchEngineComboBox.setItemText(5, QCoreApplication.translate("Preferences", u"Bing", None))

        self.label_3.setText(QCoreApplication.translate("Preferences", u"Choose which search engine is used when you search from the address bar. You can also choose a custom search engine. Use `{query}` where your search terms should go.", None))
        self.useCustomSearchEngine.setText(QCoreApplication.translate("Preferences", u"Custom search engine", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.search), QCoreApplication.translate("Preferences", u"Search", None))
        self.timeFormatComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"H:M:S", None))

        self.dateFormatComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"YEAR-MONTH-DAY", None))
        self.dateFormatComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"DAY-MONTH-YEAR", None))
        self.dateFormatComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"DAY/MONTH/YEAR", None))

        self.label_10.setText(QCoreApplication.translate("Preferences", u"Time Format", None))
        self.themesComboBox.setItemText(0, QCoreApplication.translate("Preferences", u"System Default", None))
        self.themesComboBox.setItemText(1, QCoreApplication.translate("Preferences", u"Light", None))
        self.themesComboBox.setItemText(2, QCoreApplication.translate("Preferences", u"Dark", None))

        self.label_12.setText(QCoreApplication.translate("Preferences", u"**Theme**", None))
        self.label_9.setText(QCoreApplication.translate("Preferences", u"Date Format", None))
        self.label_11.setText(QCoreApplication.translate("Preferences", u"**Locale**", None))
        self.label_4.setText(QCoreApplication.translate("Preferences", u"Theme", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.appearance), QCoreApplication.translate("Preferences", u"Appearance", None))
        self.label_13.setText(QCoreApplication.translate("Preferences", u"Download Path", None))
        self.alwaysAskForDownloadPathCheckbox.setText(QCoreApplication.translate("Preferences", u"Always ask for downloaded save file name", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.downloads), QCoreApplication.translate("Preferences", u"Downloads", None))
        self.enableAdBlockerCheckbox.setText(QCoreApplication.translate("Preferences", u"Enable Ad Blocker", None))
        self.label_14.setText(QCoreApplication.translate("Preferences", u"Blocked Hosts (one per row)", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.privacy_ad_blocker), QCoreApplication.translate("Preferences", u"Privacy and Ad Blocker", None))
    # retranslateUi

