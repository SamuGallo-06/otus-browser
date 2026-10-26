from datetime import datetime
import re, platform, sys, subprocess, os
from pathlib import Path

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