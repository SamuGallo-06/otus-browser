from datetime import datetime
import re, platform, sys, subprocess, os
from pathlib import Path
from typing import Any, TYPE_CHECKING

from PySide6.QtCore import QByteArray, QFile, QIODevice, QLocale, QStandardPaths, Qt, QUrl, QUrlQuery
from PySide6.QtGui import QColor, QGuiApplication, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
import logging

from settings import LANGUAGES_DIR

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from user_settings import SettingsManager, ProfileSettings

from ui import resources_rc  #noqa: F401

def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def fmt_eta(seconds) -> str:
    if seconds is None:
        return "unknown"
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m" if h else f"{m}m {s}s"

def fmt_time(timestamp: float) -> str:
    clock = datetime.fromtimestamp(timestamp)
    from user_settings import get_app_settings
    return clock.strftime(
        f"{get_app_settings().settings.date_format} {get_app_settings().settings.time_format}"
    )

def fmt_date(timestamp: float): 
    clock = datetime.fromtimestamp(timestamp)
    from user_settings import get_app_settings
    return clock.strftime(get_app_settings().settings.date_format)

def fmt_clock(timestamp: float): 
    clock = datetime.fromtimestamp(timestamp)
    from user_settings import get_app_settings
    return clock.strftime(get_app_settings().settings.time_format)

def sanitize_filename(name: str) -> str:
    """Toglie percorsi, caratteri di controllo e nomi vuoti."""
    name = Path(name.replace("\\", "/")).name          # niente cartelle
    name = re.sub(r"[\x00-\x1f\x7f]", "", name).strip(" .")
    return name or "download"


def unique_path(directory: str, name: str) -> str:
    """Se il file esiste già, aggiunge (1), (2)... prima dell'estensione."""
    candidate = Path(directory) / name
    stem, suffix, n = candidate.stem, candidate.suffix, 1
    while candidate.exists():
        candidate = Path(directory) / f"{stem} ({n}){suffix}"
        n += 1
    return candidate.name

def open_file(filename):
    filename = os.fspath(filename)
    if sys.platform == "darwin":        
        subprocess.run(["open", filename], check=True)     # macOS
    elif sys.platform == "win32":       
        os.startfile(filename)                             # Windows
    else:                               
        subprocess.run(["xdg-open", filename], check=True) # Linux
        
def get_download_path(profile_settings: "SettingsManager[ProfileSettings]") -> Path:
    configured = profile_settings.settings.download_directory
    if configured is not None:
        custom = Path(configured).expanduser()
        if custom.is_dir():
            return custom
        logger.warning("Configured download directory does not exist: %s", custom)

    location = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.DownloadLocation
    )
    if location:
        path = Path(location)
        if path.is_dir():
            return path

    default_path = Path.home() / "Downloads"
    default_path.mkdir(parents=True, exist_ok=True)
    return default_path


def text_to_url(text: str, search_url: str) -> QUrl:
    """Address bar input can be a URL or a search query. This function determines which it is and returns the appropriate QUrl."""
    looks_like_address = " " not in text and (
        "://" in text or "." in text or text.startswith("localhost")
    )
    if looks_like_address:
        url = QUrl.fromUserInput(text)
        if url.isValid():
            # fromUserInput usa http se manca lo schema: per un browser
            # privacy meglio https (localhost escluso)
            if "://" not in text and url.scheme() == "http" and url.host() != "localhost":
                url.setScheme("https")
            return url

    query = QUrlQuery()
    query.addQueryItem("q", text)
    url = QUrl(search_url)
    url.setQuery(query)
    return url

def to_str(value: Any) -> str:
    """Convert a settings value to the string stored in the INI file."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "auto"
    if isinstance(value, (list, tuple)):
        return "\n" + "\n".join(str(v) for v in value)
    return str(value)

_TRUE_VALUES = {"true", "yes", "on", "1"}
_FALSE_VALUES = {"false", "no", "off", "0"}

def from_str(value: str, default: Any) -> Any:
    """Convert a raw INI string to the same type as `default`.

    Raises ValueError if the string cannot be converted, so the caller
    can keep the default for that single key.
    """
    # bool must be checked before int: bool is a subclass of int
    if isinstance(default, bool):
        v = value.strip().lower()
        if v in _TRUE_VALUES:
            return True
        if v in _FALSE_VALUES:
            return False
        raise ValueError(f"Not a boolean: {value!r}")

    if isinstance(default, int):
        return int(value.strip())

    if isinstance(default, float):
        return float(value.strip())

    # One item per line; blank lines are dropped, so "" -> []
    if isinstance(default, (list, tuple)):
        items = [line.strip() for line in value.splitlines() if line.strip()]
        return tuple(items) if isinstance(default, tuple) else items

    if isinstance(default, Path):
        return Path(value.strip()).expanduser()

    # Optional values (default None): "auto" or empty means "not set"
    if default is None:
        v = value.strip()
        return None if v.lower() in ("", "auto") else v

    # Plain strings
    return value.strip()

def discover_languages() -> dict[str, str]:
    """Return {locale_key: display_name} for every valid language folder."""
    # The source strings are English, so English is always available (no file needed)
    languages = {"en_US": "English"}

    if not LANGUAGES_DIR.is_dir():       # iterdir() would raise if the folder is missing
        return languages

    for entry in sorted(LANGUAGES_DIR.iterdir()):
        if not entry.is_dir() or not (entry / "otus.qm").is_file():
            continue

        locale = QLocale(entry.name)
        if locale.language() == QLocale.Language.C:   # folder name is not a valid locale
            continue

        languages[entry.name] = locale.nativeLanguageName().capitalize()

    return languages