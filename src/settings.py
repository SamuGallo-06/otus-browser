from pathlib import Path

SEARCH_URL = "https://duckduckgo.com/"
HOME_URL = "https://duckduckgo.com"
PERSISTENT_STORAGE_PATH = Path.home() / ".local" / "share" / "OtusBrowser"
PROFILES_DIR = PERSISTENT_STORAGE_PATH / "Profiles"

ASK_FOR_PROFILE_CHOOSE = True  # If True, the user will be prompted to choose a profile on startup. If False, the default profile will be used.

LOG_FILE_PATH = PERSISTENT_STORAGE_PATH / "logs"

RISKY_DOWNLOAD_EXTENSIONS = {".appimage", ".sh", ".exe", ".jar", ".desktop"}

SUPPORTED_OPEN_FILE_EXTENSIONS = {".html", ".htm", ".xhtml", ".mhtml", ".mht"}

DEFAULT_PROFILE = "OtusProfile"  # The default profile name to use when ASK_FOR_PROFILE_CHOOSE is False.

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILES_XML_PATH = PROJECT_ROOT / "profiles.xml"

def get_download_path() -> Path:
    xdg_config = Path.home() / ".config" / "user-dirs.dirs"
    if xdg_config.exists():
        try:
            for line in xdg_config.read_text(encoding="utf-8").splitlines():
                if line.startswith("XDG_DOWNLOAD_DIR="):
                    path_str = line.split("=", 1)[1].strip('"').strip("'")
                    path_str = path_str.replace("$HOME", str(Path.home()))
                    download_dir = Path(path_str)
                    if download_dir.exists():
                        return download_dir
        except Exception:
            pass
            
    for name in ["Scaricati", "Downloads"]:
        fallback_path = Path.home() / name
        if fallback_path.exists():
            return fallback_path

    default_path = Path.home() / "Downloads"
    default_path.mkdir(exist_ok=True)
    return default_path
