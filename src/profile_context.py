from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject

from adblock import OtusAdBlocker
from bookmarks import BookmarkManager
from downloads import DownloadManager
from profiles import OtusProfile
from settings import ADBLOCKER_ENABLED
from utils import get_download_path
from views.history_view import HistoryManager


class ProfileContext(QObject):
    """Objects that must exist once per profile and be shared by all its windows.

    Every MainWindow opened with the same profile UID gets the same
    QWebEngineProfile (cookies, cache, sessions), ad blocker and library
    managers (bookmarks, downloads, history).
    """

    _instances: dict[str, "ProfileContext"] = {}

    @classmethod
    def for_profile(cls, profile_data: OtusProfile) -> "ProfileContext":
        """Return the context for this profile, creating it on first use."""
        ctx = cls._instances.get(profile_data.uid)
        if ctx is None:
            # The parent is the QApplication, so the context outlives any single window.
            ctx = cls(profile_data, parent=QApplication.instance())
            cls._instances[profile_data.uid] = ctx
        return ctx

    @classmethod
    def release(cls, uid: str) -> None:
        """Destroy the context of a profile (e.g. when its last window is closed)."""
        ctx = cls._instances.pop(uid, None)
        if ctx is not None:
            ctx.deleteLater()

    def __init__(self, profile_data: OtusProfile, parent=None):
        super().__init__(parent)
        self.profile_data = profile_data
        persistent = profile_data.type not in ("Nocturnal", "Guest")

        # Profile data is stored under .local/share/OtusBrowser/Profiles using the profile UID.
        # This allows the browser to maintain state across sessions.
        self.profile = QWebEngineProfile(profile_data.uid, self)
        profile_path = profile_data.storage_path
        profile_path.mkdir(parents=True, exist_ok=True)
        webengine_path = profile_path / "webengine"
        webengine_path.mkdir(parents=True, exist_ok=True)
        self.profile.setPersistentStoragePath(str(webengine_path))
        self.profile.setCachePath(str(webengine_path / "cache"))
        self.profile.setDownloadPath(str(get_download_path()))

        # The ad blocker is parented to the profile, so it lives exactly as long as the profile.
        self.ad_blocker = None
        if ADBLOCKER_ENABLED:
            self.ad_blocker = OtusAdBlocker(parent=self.profile)
            self.profile.setUrlRequestInterceptor(self.ad_blocker)

        # Profile library, shared by every window of this profile
        self.bookmarks = BookmarkManager(profile_data, persistent=persistent)
        self.downloads = DownloadManager(profile_data, persistent=persistent, parent=self)
        self.history = HistoryManager(profile_data, persistent=persistent)

        # Connected once here, NOT in every window: otherwise each download
        # would be handled N times (once per open window).
        self.profile.downloadRequested.connect(self._route_download)

    def _route_download(self, request: QWebEngineDownloadRequest):
        """Hand the download to the window that owns the page that triggered it."""
        page = request.page()
        view = QWebEngineView.forPage(page) if page is not None else None
        window = view.window() if view is not None else QApplication.activeWindow()
        if window is not None and hasattr(window, "onDownloadRequested"):
            window.onDownloadRequested(request) #type: ignore