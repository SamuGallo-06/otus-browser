from pathlib import Path
from PySide6.QtCore import QStandardPaths, Qt
import os

## Paths
PERSISTENT_STORAGE_PATH = Path.home() / ".local" / "share" / "OtusBrowser"
PROFILES_DIR = PERSISTENT_STORAGE_PATH / "Profiles"
KEYS_DIR = PERSISTENT_STORAGE_PATH / "Keys"
MOUNT_POINT = Path(os.environ["XDG_RUNTIME_DIR"]) / "otus-browser" / "{uid}"

LOG_FILE_PATH = PERSISTENT_STORAGE_PATH / "logs"
PROFILES_XML_PATH = PERSISTENT_STORAGE_PATH / "profiles.xml"

## Browser Parameters

RISKY_DOWNLOAD_EXTENSIONS = {".appimage", ".sh", ".exe", ".jar", ".desktop", ".bat", ".bin", ".run", ".deb", ".rpm", ".msi", ""}
SUPPORTED_OPEN_FILE_EXTENSIONS = {".html", ".htm", ".xhtml", ".mhtml", ".mht"}
AUTO_DOWNLOAD_DIRECTORY = "<auto>"

AVAILABLE_THEMES = {
    "light": Qt.ColorScheme.Light,
    "dark": Qt.ColorScheme.Dark,
    "system": Qt.ColorScheme.Unknown
}

##################################################################
# Browser Settings (This variable can be overridden by the user) #
##################################################################

HOME_URL = "https://duckduckgo.com"
SEARCH_URL = "https://duckduckgo.com/"

ASK_FOR_PROFILE_CHOOSE = True  # If True, the user will be prompted to choose a profile on startup. If False, the default profile will be used.
DEFAULT_PROFILE = "OtusProfile"  # The default profile name to use when ASK_FOR_PROFILE_CHOOSE is False.

ASK_FOR_DOWNLOAD_PATH = False
DOWNLOAD_DIRECTORY = AUTO_DOWNLOAD_DIRECTORY

ALWAYS_ASK_BEFORE_EXIT = True

## User Interface
DATETIME_FORMAT = "it"
LANG="it-IT"

THEME = "Light"  # Options: "Light", "Dark", "System"


def get_download_path() -> Path:
    # User override, if it is still a valid folder
    if DOWNLOAD_DIRECTORY != AUTO_DOWNLOAD_DIRECTORY:
        custom = Path(DOWNLOAD_DIRECTORY).expanduser()
        if custom.is_dir():
            return custom

    # System download folder (reads XDG user-dirs on Linux)
    location = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation)
    if location:
        path = Path(location)
        if path.is_dir():
            return path

    # Last resort
    default_path = Path.home() / "Downloads"
    default_path.mkdir(parents=True, exist_ok=True)
    return default_path