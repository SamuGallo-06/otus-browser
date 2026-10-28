import os
from pathlib import Path

from PySide6.QtCore import QStandardPaths, Qt

##################################
## Browser Parameters           ##
##################################

# Application paths
PERSISTENT_STORAGE_PATH = Path.home() / ".local" / "share" / "OtusBrowser"
PROFILES_DIR = PERSISTENT_STORAGE_PATH / "Profiles"
KEYS_DIR = PERSISTENT_STORAGE_PATH / "Keys"
MOUNT_POINT = Path(os.environ["XDG_RUNTIME_DIR"]) / "otus-browser" / "{uid}"
LOG_FILE_PATH = PERSISTENT_STORAGE_PATH / "logs"
PROFILES_XML_PATH = PERSISTENT_STORAGE_PATH / "profiles.xml"
BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "resources"
SETTINGS_PATH = PERSISTENT_STORAGE_PATH / "settings.ini"

# Browser parameters
RISKY_DOWNLOAD_EXTENSIONS = {".appimage", ".sh", ".exe", ".jar", ".desktop", ".bat", ".bin", ".run", ".deb", ".rpm", ".msi", ""}
SUPPORTED_OPEN_FILE_EXTENSIONS = {".html", ".htm", ".xhtml", ".mhtml", ".mht"}
AUTO_DOWNLOAD_DIRECTORY = "<auto>"
AVAILABLE_THEMES = {
    "light": Qt.ColorScheme.Light,
    "dark": Qt.ColorScheme.Dark,
    "system": Qt.ColorScheme.Unknown,
}

FEATHER_ICON_PACK = ":feather/resources/feather/"
OTUS_ICON_PACK = ":otus/resources/"

##################################
## User-configurable settings   ##
##################################

## Ad-blocker settings

DEFAULT_BLOCKED_HOSTS = (
    "doubleclick.net",
    "googlesyndication.com",
    "googletagservices.com",
    "analytics.tiktok.com",
)
##################################
## Helpers                      ##
##################################


def get_download_path() -> Path:
    # Fall back to the system download folder (including XDG user-dirs on Linux).
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
    if location:
        path = Path(location)
        if path.is_dir():
            return path

    # Create and use the default download folder as a last resort.
    default_path = Path.home() / "Downloads"
    default_path.mkdir(parents=True, exist_ok=True)
    return default_path
