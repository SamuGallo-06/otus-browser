from datetime import datetime
import re, platform, sys, subprocess, os
from pathlib import Path
from settings import *

from PySide6.QtCore import QByteArray, QFile, QIODevice, Qt, QUrl, QUrlQuery
from PySide6.QtGui import QColor, QGuiApplication, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

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
    
    return clock.strftime("%d/%m/%Y %H:%M:%S")

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
        
def text_to_url(text: str) -> QUrl:
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
    url = QUrl(SEARCH_URL)
    url.setQuery(query)
    return url