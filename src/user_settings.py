# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Samuele Gallicani

import configparser
import logging
import re
from gettext import gettext as gtr
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Any, ClassVar, Generic, Protocol, TypeVar

from PySide6.QtCore import QObject, Signal

from settings import DEFAULT_BLOCKED_HOSTS, AVAILABLE_THEMES
from utils import from_str, to_str

logger = logging.getLogger(__name__)

class DataclassSettings(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Any]]


T = TypeVar("T", bound=DataclassSettings)


# fmt: off
@dataclass
class AppSettings:
    # Name                         | type       | default                       | metadata
    ask_for_profile_choose:         bool = field(default=True,                 metadata={"section": "general"})
    default_profile:                str = field(default="OtusProfile",         metadata={"section": "general"})
    always_ask_before_exit:         bool = field(default=True,                 metadata={"section": "general"})
    theme:                          str = field(default="dark",                metadata={"section": "appearance"})
    lang:                           str = field(default="it_IT",               metadata={"section": "appearance"})
    date_format:                    str = field(default="%d/%m/%Y",            metadata={"section": "appearance"})
    time_format:                    str = field(default="%H:%M:%S",            metadata={"section": "appearance"})

    def __post_init__(self) -> None:
        normalized = self.theme.strip().lower()
        if normalized not in AVAILABLE_THEMES:
            logger.warning(gtr("Unknown theme %r, using dark"), self.theme)
            self.theme = "dark"
        else:
            self.theme = normalized


@dataclass
class ProfileSettings:
    # Name                         | type              | default                           | metadata
    home_url:                       str = field(default="https://duckduckgo.com",            metadata={"section": "general"})
    search_url:                     str = field(default="https://duckduckgo.com/?q={query}", metadata={"section": "general"})
    restore_previous_session:       bool = field(default=False,                              metadata={"section": "startup"})
    use_startup_pages:              bool = field(default=False,                              metadata={"section": "startup"})
    startup_pages:                  list[str] = field(default_factory=list,                  metadata={"section": "startup"})
    ask_for_download_path:          bool = field(default=False,                              metadata={"section": "downloads"})
    download_directory:             str | None = field(default=None,                         metadata={"section": "downloads"})
    adblocker_enabled:              bool = field(default=True,                               metadata={"section": "adblocker"})
    blocked_hosts:                  list[str] = field(default_factory=lambda: list(DEFAULT_BLOCKED_HOSTS), metadata={"section": "adblocker"})
    show_tracker_count:             bool = field(default=True,                               metadata={"section": "privacy"})

    def __post_init__(self) -> None:
        normalized_hosts: list[str] = []
        for host in self.blocked_hosts:
            value = re.sub(r"^https?://", "", host.strip(), flags=re.IGNORECASE)
            value = value.split("/", 1)[0].split(":", 1)[0].strip().lower()
            if value and value not in normalized_hosts:
                normalized_hosts.append(value)
        self.blocked_hosts = normalized_hosts

# fmt: on


class SettingsManager(QObject, Generic[T]):
    settingsChanged = Signal()

    def __init__(
        self,
        config_path: Path,
        settings_cls: type[T],
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.config_path = config_path
        self._cls = settings_cls
        self._closed = False
        first_run = not config_path.exists()
        self._settings = self.deserialize()
        if first_run:
            self.serialize()

    @property
    def settings(self) -> T:
        return self._settings

    def serialize(self, obj: T | None = None) -> None:
        if self._closed:
            logger.warning(
                gtr("Cannot serialize closed settings manager: %s"),
                self.config_path,
            )
            return
        obj = obj if obj is not None else self._settings
        config = configparser.ConfigParser(interpolation=None)
        for setting in fields(obj):
            section = setting.metadata["section"]
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, setting.name, to_str(getattr(obj, setting.name)))

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.config_path.with_suffix(".ini.tmp")
        with temporary_path.open("w", encoding="utf-8") as file:
            config.write(file)
        temporary_path.replace(self.config_path)

    def deserialize(self) -> T:
        defaults = self._cls()
        if not self.config_path.exists():
            return defaults

        config = configparser.ConfigParser(interpolation=None)
        try:
            config.read(self.config_path, encoding="utf-8")
        except configparser.Error:
            logger.warning(
                gtr("Corrupted settings file, backing it up and using defaults")
            )
            self.config_path.replace(self.config_path.with_suffix(".ini.bak"))
            return defaults

        values: dict[str, object] = {}
        for setting in fields(defaults):
            section = setting.metadata["section"]
            if not config.has_option(section, setting.name):
                continue
            try:
                values[setting.name] = from_str(
                    config.get(section, setting.name),
                    getattr(defaults, setting.name),
                )
            except ValueError:
                logger.warning(
                    gtr("Invalid value for %s.%s, using default"),
                    section,
                    setting.name,
                )
        return self._cls(**values)

    def update(self, new_settings: T) -> None:
        if self._closed:
            logger.warning(
                gtr("Cannot update closed settings manager: %s"),
                self.config_path,
            )
            return
        self.serialize(new_settings)
        self._settings = new_settings
        self.settingsChanged.emit()

    def reset_to_defaults(self) -> None:
        self.update(self._cls())

    def close(self) -> None:
        self._closed = True


_app_settings: SettingsManager[AppSettings] | None = None


def init_app_settings(
    path: Path, parent: QObject | None = None
) -> SettingsManager[AppSettings]:
    """Create the single application-level manager. Call once in main.py, after QApplication."""
    global _app_settings
    _app_settings = SettingsManager(path, AppSettings, parent)
    return _app_settings


def get_app_settings() -> SettingsManager[AppSettings]:
    """Return the application-level manager (raises if init_app_settings was not called)."""
    if _app_settings is None:
        raise RuntimeError("App settings not initialised: call init_app_settings() first")
    return _app_settings
