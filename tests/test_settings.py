# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Samuele Gallicani

import sys
from pathlib import Path

import pytest
from PySide6.QtCore import QCoreApplication

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from user_settings import AppSettings, ProfileSettings, SettingsManager


@pytest.fixture(scope="session")
def qt_app() -> QCoreApplication:
    return QCoreApplication.instance() or QCoreApplication([])


def test_round_trip_defaults(tmp_path: Path, qt_app: QCoreApplication) -> None:
    app_path = tmp_path / "app.ini"
    profile_path = tmp_path / "profile.ini"
    app = SettingsManager(app_path, AppSettings)
    profile = SettingsManager(profile_path, ProfileSettings)

    assert SettingsManager(app_path, AppSettings).settings == app.settings
    assert SettingsManager(profile_path, ProfileSettings).settings == profile.settings


def test_round_trip_awkward_values(tmp_path: Path, qt_app: QCoreApplication) -> None:
    app_path = tmp_path / "app.ini"
    profile_path = tmp_path / "profile.ini"
    app = SettingsManager(app_path, AppSettings)
    profile = SettingsManager(profile_path, ProfileSettings)
    app.update(
        AppSettings(
            date_format="%d/%m/%Y",
            ask_for_profile_choose=False,
            always_ask_before_exit=False,
        )
    )
    profile.update(
        ProfileSettings(
            download_directory=None,
            blocked_hosts=[],
            search_url="https://example.test/?q={query}",
            ask_for_download_path=True,
            adblocker_enabled=False,
        )
    )

    assert SettingsManager(app_path, AppSettings).settings.date_format == "%d/%m/%Y"
    assert SettingsManager(app_path, AppSettings).settings.ask_for_profile_choose is False
    loaded = SettingsManager(profile_path, ProfileSettings).settings
    assert loaded.download_directory is None
    assert loaded.blocked_hosts == []
    assert loaded.search_url == "https://example.test/?q={query}"
    assert loaded.ask_for_download_path is True
    assert loaded.adblocker_enabled is False


def test_first_run_creates_defaults(tmp_path: Path, qt_app: QCoreApplication) -> None:
    path = tmp_path / "new.ini"
    manager = SettingsManager(path, AppSettings)

    assert path.exists()
    assert manager.settings == AppSettings()


def test_invalid_boolean_keeps_only_that_default(tmp_path: Path, qt_app: QCoreApplication) -> None:
    path = tmp_path / "profile.ini"
    path.write_text(
        "[general]\n"
        "home_url = https://example.test\n"
        "[downloads]\n"
        "ask_for_download_path = true\n"
        "[adblocker]\n"
        "adblocker_enabled = forse\n",
        encoding="utf-8",
    )

    settings = SettingsManager(path, ProfileSettings).settings

    assert settings.adblocker_enabled is True
    assert settings.home_url == "https://example.test"
    assert settings.ask_for_download_path is True


def test_capitalized_boolean_is_true(tmp_path: Path, qt_app: QCoreApplication) -> None:
    path = tmp_path / "profile.ini"
    path.write_text("[adblocker]\nadblocker_enabled = Yes\n", encoding="utf-8")

    assert SettingsManager(path, ProfileSettings).settings.adblocker_enabled is True


def test_corrupted_file_is_backed_up(tmp_path: Path, qt_app: QCoreApplication) -> None:
    path = tmp_path / "profile.ini"
    path.write_text("not an ini section", encoding="utf-8")

    manager = SettingsManager(path, ProfileSettings)

    assert manager.settings == ProfileSettings()
    assert not path.exists()
    assert path.with_suffix(".ini.bak").read_text(encoding="utf-8") == "not an ini section"


def test_unknown_values_are_ignored(tmp_path: Path, qt_app: QCoreApplication) -> None:
    path = tmp_path / "app.ini"
    path.write_text(
        "[general]\n"
        "unknown = ignored\n"
        "[unknown]\n"
        "value = ignored\n",
        encoding="utf-8",
    )

    assert SettingsManager(path, AppSettings).settings == AppSettings()


def test_update_replaces_settings_and_emits_once(
    tmp_path: Path, qt_app: QCoreApplication
) -> None:
    path = tmp_path / "app.ini"
    manager = SettingsManager(path, AppSettings)
    emitted: list[None] = []
    manager.settingsChanged.connect(lambda: emitted.append(None))
    new_settings = AppSettings(default_profile="NewProfile")

    manager.update(new_settings)

    assert manager.settings == new_settings
    assert SettingsManager(path, AppSettings).settings == new_settings
    assert len(emitted) == 1


def test_close_prevents_update_from_modifying_file(
    tmp_path: Path, qt_app: QCoreApplication
) -> None:
    path = tmp_path / "app.ini"
    manager = SettingsManager(path, AppSettings)
    original = path.read_text(encoding="utf-8")
    manager.close()

    manager.update(AppSettings(default_profile="Changed"))

    assert path.read_text(encoding="utf-8") == original
    assert manager.settings == AppSettings()


def test_settings_normalize_values() -> None:
    assert AppSettings(theme="rosa").theme == "dark"
    assert ProfileSettings(
        blocked_hosts=["HTTPS://DoubleClick.net/x", "doubleclick.net", ""]
    ).blocked_hosts == ["doubleclick.net"]
