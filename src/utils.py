from datetime import datetime
import re, platform, sys, subprocess, os
from pathlib import Path
from typing import Any, TYPE_CHECKING

from PySide6.QtCore import QByteArray, QFile, QIODevice, QLocale, QStandardPaths, Qt, QUrl, QUrlQuery
from PySide6.QtGui import QColor, QGuiApplication, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
import logging

from settings import LANGUAGES_PATH

logger = logging.getLogger(__name__)

# Tracking parameters removed when SilentWing cleans a top-level URL.
TRACKING_PARAMS = {
    "fbclid", "gclid", "dclid", "msclkid", "yclid", "igshid",
    "mc_cid", "mc_eid", "_hsenc", "_hsmi",
}


def clean_url(url: QUrl) -> QUrl:
    """Return a copy of the URL without common tracking parameters."""
    query = QUrlQuery(url)
    removed = False
    for key, _value in query.queryItems():
        if key.lower().startswith("utm_") or key.lower() in TRACKING_PARAMS:
            query.removeAllQueryItems(key)
            removed = True
    if not removed:
        return url

    cleaned = QUrl(url)
    if query.isEmpty():
        cleaned.setQuery("")
    else:
        cleaned.setQuery(query)
    return cleaned


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
    """Convert a settings value to the string stored in tP =he INI file."""
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

def normalize_language_code(code: str) -> str:
    """Return a canonical language code such as ``it_IT``."""
    parts = code.strip().replace("-", "_").split("_", 1)
    language = parts[0].lower()
    if not language:
        return ""
    return (
        f"{language}_{parts[1].upper()}"
        if len(parts) == 2 and parts[1]
        else language
    )


def language_candidates(code: str) -> list[str]:
    """Return language fallbacks from most specific to English."""
    normalized = normalize_language_code(code)
    candidates = [normalized] if normalized else []
    if "_" in normalized:
        candidates.append(normalized.split("_", 1)[0])
    if "en" not in candidates:
        candidates.append("en")
    return candidates


def discover_languages(base: Path = LANGUAGES_PATH) -> dict[str, str]:
    """Return {locale_key: display_name} for installed translations."""
    # English is the source language, so it is always available without a catalog.
    languages = {"en_US": "English"}
    for code in find_installed_languages(base):
        locale = QLocale(code)
        languages[code] = locale.nativeLanguageName().capitalize()

    return languages

def find_installed_languages(base: Path = LANGUAGES_PATH) -> dict[str, Path]:
    """Return {lang_code: dir} for every installed application translation."""
    if not base.is_dir():
        return {}

    languages: dict[str, Path] = {}
    for directory in sorted(base.iterdir()):
        if not directory.is_dir():
            continue
        code = normalize_language_code(directory.name)
        if not code or QLocale(code).language() == QLocale.Language.C:
            continue
        if (directory / f"otus_browser_{directory.name}.qm").is_file():
            languages.setdefault(code, directory)
    return languages