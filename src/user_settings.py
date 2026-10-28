from dataclasses import dataclass, field, fields
from pathlib import Path
from settings import DEFAULT_BLOCKED_HOSTS
import configparser
from logging import getLogger
from PySide6.QtCore import Signal, QObject

logger = getLogger(__name__)

from utils import to_str, from_str

# fmt: off
@dataclass
class UserSettings:
    #Name                   | type               | default                                            |  metadata       
    # General
    home_url:                        str = field( default="https://duckduckgo.com",                    metadata={"section": "general"})
    search_url:                      str = field( default="https://duckduckgo.com",                    metadata={"section": "general"})
    ask_for_profile_choose:         bool = field( default=True,                                        metadata={"section": "general"})
    default_profile:                 str = field( default="OtusProfile",                               metadata={"section": "general"})
    always_ask_before_exit:         bool = field( default=True,                                        metadata={"section": "general"})
    
    # Downloads
    ask_for_download_path:          bool = field( default=False,                                       metadata={"section": "downloads"})
    download_directory:       str | None = field( default=None,                                        metadata={"section": "downloads"})   # None = automatic XDG path
    
    # Appearance
    theme:                           str = field( default="dark",                                      metadata={"section": "appearance"})  # key of AVAILABLE_THEMES
    lang:                            str = field( default="it-IT",                                     metadata={"section": "appearance"})
    date_format:                     str = field( default="%d/%m/%Y",                                  metadata={"section": "appearance"})
    time_format:                     str = field( default="%H:%M:%S",                                  metadata={"section": "appearance"})
    
    # Ad blocker
    adblocker_enabled:              bool = field( default=True,                                        metadata={"section": "adblocker"})
    blocked_hosts:             list[str] = field( default_factory=lambda: list(DEFAULT_BLOCKED_HOSTS), metadata={"section": "adblocker"})
    
# fmt: on

class UserSettingsManager(QObject):
    
    settingsChanged = Signal()
        
    @property
    def settings(self) -> UserSettings:
        return self._settings
        
            
    def __init__(self, config_path: Path, parent=None):
        super().__init__(parent)
        self.config_path = config_path
        first_run = not config_path.exists()
        self._settings = self.deserialize()   # returns defaults if the file is missing/corrupted
        if first_run:
            self.serialize()                  # write the defaults only on first run

    def serialize(self, obj: UserSettings | None = None) -> None:
        """Write the given settings (default: the current ones) to the INI file."""
        obj = obj if obj is not None else self._settings
        config = configparser.ConfigParser(interpolation=None)   # empty: the file mirrors the settings
        for f in fields(obj):
            section = f.metadata["section"]
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, f.name, to_str(getattr(obj, f.name)))

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.config_path.with_suffix(".ini.tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            config.write(fh)
        tmp.replace(self.config_path)               # atomic on the same filesystem

    def deserialize(self) -> UserSettings:
        """Read the INI file and return a UserSettings (defaults for anything missing/invalid)."""
        defaults = UserSettings()                   # NOT self._settings: it may not exist yet
        if not self.config_path.exists():
            return defaults

        config = configparser.ConfigParser(interpolation=None)
        try:
            config.read(self.config_path, encoding="utf-8")
        except configparser.Error:
            logger.warning("Corrupted settings file, backing it up and using defaults")
            self.config_path.replace(self.config_path.with_suffix(".ini.bak"))
            return defaults

        values = {}
        for f in fields(defaults):
            section = f.metadata["section"]
            if not config.has_option(section, f.name):
                continue                            # missing key: keep the default
            try:
                values[f.name] = from_str(config.get(section, f.name), getattr(defaults, f.name))
            except ValueError:
                logger.warning("Invalid value for %s.%s, using default", section, f.name)
        return UserSettings(**values)
    
    def update(self, new_settings: UserSettings) -> None:
        self.serialize(new_settings)        # write first: if it fails, the state is unchanged
        self._settings = new_settings
        self.settingsChanged.emit()
        
        
_manager: UserSettingsManager | None = None

def init_settings(path: Path, parent: QObject | None = None) -> UserSettingsManager:
    """Create the single manager. Call once, in main.py, after QApplication."""
    global _manager
    _manager = UserSettingsManager(path, parent)
    return _manager

def get_settings_manager() -> UserSettingsManager:
    if _manager is None:
        raise RuntimeError("Settings not initialised: call init_settings() first")
    return _manager
                    
        
            
                
            
            

