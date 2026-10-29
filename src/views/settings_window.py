# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Samuele Gallicani

from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from profiles import get_profiles
from settings import AVAILABLE_THEMES, DATE_FORMAT_PRESETS, TIME_FORMAT_PRESETS
from ui.ui_preferences import Ui_Preferences
from user_settings import (
    AppSettings,
    ProfileSettings,
    SettingsManager,
    get_app_settings,
)
from utils import discover_languages


SEARCH_ENGINES = {
    "DuckDuckGo (Suggested)": "https://duckduckgo.com/?q={query}",
    "Brave Search": "https://search.brave.com/search?q={query}",
    "Qwant": "https://www.qwant.com/?q={query}",
    "Startpage": "https://www.startpage.com/sp/search?query={query}",
    "Google": "https://www.google.com/search?q={query}",
    "Bing": "https://www.bing.com/search?q={query}",
}


class SettingsWindow(QWidget):
    settingsChanged = Signal()

    def __init__(
        self,
        profile_settings: SettingsManager[ProfileSettings],
        parent=None,
    ):
        super().__init__(parent)
        self.ui = Ui_Preferences()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.Window)
        self.global_settings = get_app_settings()
        self.profile_settings = profile_settings
        self.ui.toolBox.setCurrentIndex(0)
        self.populate_settings()
        self.ui.applyButton.clicked.connect(self.apply_settings)
        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.restoreDefaultsButton.clicked.connect(self.restore_defaults)
        self.ui.useCustomSearchEngine.toggled.connect(
            self.ui.customSearchEngineField.setEnabled
        )

    def populate_settings(self) -> None:
        app: AppSettings = self.global_settings.settings
        profile: ProfileSettings = self.profile_settings.settings

        self.ui.languageComboBox.clear()
        for key, label in discover_languages().items():
            self.ui.languageComboBox.addItem(label, key)
        self.ui.languageComboBox.setCurrentIndex(
            max(0, self.ui.languageComboBox.findData(app.lang))
        )

        self.ui.themesComboBox.clear()
        for key in AVAILABLE_THEMES:
            self.ui.themesComboBox.addItem(key.capitalize(), key)
        self.ui.themesComboBox.setCurrentIndex(
            max(0, self.ui.themesComboBox.findData(app.theme))
        )

        now = datetime.now()
        self.ui.dateFormatComboBox.clear()
        for preset in DATE_FORMAT_PRESETS:
            self.ui.dateFormatComboBox.addItem(now.strftime(preset), preset)
        self.ui.dateFormatComboBox.setCurrentIndex(
            max(0, self.ui.dateFormatComboBox.findData(app.date_format))
        )

        self.ui.timeFormatComboBox.clear()
        for preset in TIME_FORMAT_PRESETS:
            self.ui.timeFormatComboBox.addItem(now.strftime(preset), preset)
        self.ui.timeFormatComboBox.setCurrentIndex(
            max(0, self.ui.timeFormatComboBox.findData(app.time_format))
        )

        self.ui.profilesComboBox.clear()
        for profile_entry in get_profiles().values():
            if not profile_entry.hidden:
                self.ui.profilesComboBox.addItem(profile_entry.name, profile_entry.uid)
        self.ui.profilesComboBox.setCurrentIndex(
            max(0, self.ui.profilesComboBox.findData(app.default_profile))
        )

        self.ui.askForProfileChooseCheckbox.setChecked(app.ask_for_profile_choose)
        self.ui.alwaysAskBeforeExitCheckbox.setChecked(app.always_ask_before_exit)
        self.ui.restoreSessionRadioButton.setChecked(
            profile.restore_previous_session
        )
        self.ui.useStartupPagesRadioButton.setChecked(
            not profile.restore_previous_session and profile.use_startup_pages
        )
        self.ui.emptyTabRadioButton.setChecked(
            not profile.restore_previous_session and not profile.use_startup_pages
        )
        self.ui.startupPages.setPlainText("\n".join(profile.startup_pages))
        self.ui.homePageUrlField.setText(profile.home_url)

        self.ui.searchEngineComboBox.clear()
        for label in SEARCH_ENGINES:
            self.ui.searchEngineComboBox.addItem(label, SEARCH_ENGINES[label])
        search_index = self.ui.searchEngineComboBox.findData(profile.search_url)
        if search_index >= 0:
            self.ui.searchEngineComboBox.setCurrentIndex(search_index)
            self.ui.useCustomSearchEngine.setChecked(False)
            self.ui.customSearchEngineField.clear()
        else:
            self.ui.useCustomSearchEngine.setChecked(True)
            self.ui.customSearchEngineField.setText(profile.search_url)
        self.ui.customSearchEngineField.setEnabled(
            self.ui.useCustomSearchEngine.isChecked()
        )

        self.ui.downloadPathField.setText(profile.download_directory or "")
        self.ui.alwaysAskForDownloadPathCheckbox.setChecked(
            profile.ask_for_download_path
        )
        self.ui.enableAdBlockerCheckbox.setChecked(profile.adblocker_enabled)
        self.ui.showTrackerCountCheckbox.setChecked(profile.show_tracker_count)
        self.ui.blockedHostsEntry.setPlainText("\n".join(profile.blocked_hosts))

    def apply_settings(self) -> None:
        app = self.global_settings.settings
        profile = self.profile_settings.settings

        search_url = (
            self.ui.customSearchEngineField.text().strip()
            if self.ui.useCustomSearchEngine.isChecked()
            else self.ui.searchEngineComboBox.currentData()
        )
        if not search_url:
            search_url = profile.search_url

        selected_profile = self.ui.profilesComboBox.currentData()
        new_app_settings = AppSettings(
            ask_for_profile_choose=self.ui.askForProfileChooseCheckbox.isChecked(),
            default_profile=selected_profile or app.default_profile,
            always_ask_before_exit=self.ui.alwaysAskBeforeExitCheckbox.isChecked(),
            theme=self.ui.themesComboBox.currentData() or app.theme,
            lang=self.ui.languageComboBox.currentData() or app.lang,
            date_format=self.ui.dateFormatComboBox.currentData() or app.date_format,
            time_format=self.ui.timeFormatComboBox.currentData() or app.time_format,
        )
        new_profile_settings = ProfileSettings(
            home_url=self.ui.homePageUrlField.text().strip() or profile.home_url,
            restore_previous_session=self.ui.restoreSessionRadioButton.isChecked(),
            use_startup_pages=self.ui.useStartupPagesRadioButton.isChecked(),
            startup_pages=[
                page.strip()
                for page in self.ui.startupPages.toPlainText().splitlines()
                if page.strip()
            ],
            search_url=search_url,
            ask_for_download_path=(
                self.ui.alwaysAskForDownloadPathCheckbox.isChecked()
            ),
            download_directory=self.ui.downloadPathField.text().strip() or None,
            adblocker_enabled=self.ui.enableAdBlockerCheckbox.isChecked(),
            blocked_hosts=self.ui.blockedHostsEntry.toPlainText().splitlines(),
            show_tracker_count=self.ui.showTrackerCountCheckbox.isChecked(),
        )

        self.global_settings.update(new_app_settings)
        self.profile_settings.update(new_profile_settings)
        self.settingsChanged.emit()
        self.close()

    def restore_defaults(self) -> None:
        self.global_settings.reset_to_defaults()
        self.profile_settings.reset_to_defaults()
        self.populate_settings()
