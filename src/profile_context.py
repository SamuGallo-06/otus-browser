from PySide6.QtWebEngineCore import QWebEngineDownloadRequest, QWebEngineProfile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal

from adblock import AdBlockPolicy
from bookmarks import BookmarkManager
from downloads import DownloadManager
from interceptor import OtusRequestInterceptor
from profiles import OtusProfile
from silentwing import SilentWing
from user_settings import ProfileSettings, SettingsManager
from utils import get_download_path
from views.history_view import HistoryManager


class ProfileContext(QObject):
    """Objects that must exist once per profile and be shared by all its windows.

    Every MainWindow opened with the same profile UID gets the same
    QWebEngineProfile (cookies, cache, sessions), ad blocker and library
    managers (bookmarks, downloads, history).
    """

    _instances: dict[str, "ProfileContext"] = {}
    silentWingChanged = Signal(bool)
    blockedCountChanged = Signal(int)

    @classmethod
    def for_profile(
        cls,
        profile_data: OtusProfile,
        profile_settings: SettingsManager[ProfileSettings],
    ) -> "ProfileContext":
        """Return the context for this profile, creating it on first use."""
        ctx = cls._instances.get(profile_data.uid)
        if ctx is None:
            # The parent is the QApplication, so the context outlives any single window.
            ctx = cls(profile_data, profile_settings, parent=QApplication.instance())
            cls._instances[profile_data.uid] = ctx
        return ctx

    @classmethod
    def release(cls, uid: str) -> None:
        """Destroy the context of a profile (e.g. when its last window is closed)."""
        ctx = cls._instances.pop(uid, None)
        if ctx is not None:
            ctx.deleteLater()

    def __init__(
        self,
        profile_data: OtusProfile,
        profile_settings: SettingsManager[ProfileSettings],
        parent=None,
    ):
        super().__init__(parent)
        self.profile_data = profile_data
        self.profile_settings = profile_settings
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
        self.profile.setDownloadPath(str(get_download_path(profile_settings)))
        profile_settings.settingsChanged.connect(
            lambda: self.profile.setDownloadPath(str(get_download_path(profile_settings)))
        )

        # Policies are owned by the interceptor, which is parented to the profile.
        self.adblock_policy = AdBlockPolicy(profile_settings)
        self.silent_wing_policy = SilentWing()
        self.interceptor = OtusRequestInterceptor(
            [self.adblock_policy, self.silent_wing_policy],
            parent=self.profile,
        )
        self.profile.setUrlRequestInterceptor(self.interceptor)
        self.total_blocked_count = 0
        self.interceptor.requestBlocked.connect(self._on_request_blocked)
        profile_settings.settingsChanged.connect(
            lambda: self.adblock_policy.refresh(profile_settings.settings)
        )

        # Profile library, shared by every window of this profile
        self.bookmarks = BookmarkManager(profile_data, persistent=persistent)
        self.downloads = DownloadManager(
            profile_data, profile_settings, persistent=persistent, parent=self
        )
        self.history = HistoryManager(profile_data, persistent=persistent)

        # Connected once here, NOT in every window: otherwise each download
        # would be handled N times (once per open window).
        self.profile.downloadRequested.connect(self._route_download)

    def set_silent_wing_enabled(self, enabled: bool) -> None:
        if self.silent_wing_policy.enabled == enabled:
            return
        self.silent_wing_policy.enabled = enabled
        self.silentWingChanged.emit(enabled)

    def _on_request_blocked(self) -> None:
        self.total_blocked_count += 1
        self.blockedCountChanged.emit(self.total_blocked_count)

    def _route_download(self, request: QWebEngineDownloadRequest):
        """Hand the download to the window that owns the page that triggered it."""
        page = request.page()
        view = QWebEngineView.forPage(page) if page is not None else None
        window = view.window() if view is not None else QApplication.activeWindow()
        if window is not None and hasattr(window, "onDownloadRequested"):
            window.onDownloadRequested(request) #type: ignore