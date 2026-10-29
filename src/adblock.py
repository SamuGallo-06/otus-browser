"""Ad-blocking request policy for Otus Browser."""

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInfo

from user_settings import ProfileSettings, SettingsManager


class AdBlockPolicy:
    """Blocks requests to configured advertising and tracking hosts."""

    def __init__(
        self,
        profile_settings: SettingsManager[ProfileSettings],
    ):
        self.blocked_count = 0
        self.enabled = True
        self._exact: frozenset[str] = frozenset()

        self.refresh(profile_settings.settings)

    def refresh(self, settings: ProfileSettings) -> None:
        """Apply the current ad-blocking settings."""
        self.enabled = settings.adblocker_enabled
        self._exact = frozenset(settings.blocked_hosts)

    def apply(
        self,
        info: QWebEngineUrlRequestInfo,
        url: QUrl,
        host: str,
    ) -> bool:
        """Block the request when its host matches a configured host."""
        del url

        if host in self._exact:
            self._block(info)
            return True

        if any(host.endswith(f".{blocked}") for blocked in self._exact):
            self._block(info)
            return True

        return False

    def _block(self, info: QWebEngineUrlRequestInfo) -> None:
        self.blocked_count += 1
        info.block(True)