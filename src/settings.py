from pathlib import Path

SEARCH_URL = "https://duckduckgo.com/"
HOME_URL = "https://duckduckgo.com"
PERSISTENT_STORAGE_PATH = Path.home() / ".local" / "share" / "OtusBrowser"
PROFILES_DIR = PERSISTENT_STORAGE_PATH / "Profiles"

ASK_FOR_PROFILE_CHOOSE = False  # If True, the user will be prompted to choose a profile on startup. If False, the default profile will be used.