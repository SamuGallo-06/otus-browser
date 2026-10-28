"""Minimal host-based request blocker for Otus Browser."""

from PySide6.QtCore import QObject
from PySide6.QtWebEngineCore import (
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)
from user_settings import ProfileSettings, SettingsManager

class OtusAdBlocker(QWebEngineUrlRequestInterceptor):
    """Blocks requests to a list of ad and tracking hosts."""

    def __init__(
        self,
        profile_settings: SettingsManager[ProfileSettings],
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.blocked_count = 0
        self._enabled = True
        self._exact: frozenset[str] = frozenset()
        self.refresh(profile_settings.settings)

    def refresh(self, settings: ProfileSettings) -> None:
        self._enabled = settings.adblocker_enabled
        self._exact = frozenset(settings.blocked_hosts)

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        # Runs on the IO thread: never touch widgets or other GUI objects here.
        if not self._enabled:
            return
        host = info.requestUrl().host().lower()
        if host in self._exact or any(host.endswith("." + blocked) for blocked in self._exact):
            self.blocked_count += 1
            info.block(True)