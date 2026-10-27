"""Minimal host-based request blocker for Otus Browser."""

from settings import DEFAULT_BLOCKED_HOSTS

from PySide6.QtCore import QObject
from PySide6.QtWebEngineCore import (
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)

class OtusAdBlocker(QWebEngineUrlRequestInterceptor):
    """Blocks requests to a list of ad and tracking hosts."""

    def __init__(self, hosts=None, parent: QObject | None = None):
        super().__init__(parent)
        if hosts is None:
            hosts = DEFAULT_BLOCKED_HOSTS  # imported from settings
        cleaned = {h.strip().lower().lstrip(".") for h in hosts if h and h.strip()}
        self._exact = frozenset(cleaned)
        self._subdomains = tuple("." + h for h in cleaned)
        self.blocked_count = 0

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        # Runs on the IO thread: never touch widgets or other GUI objects here.
        host = info.requestUrl().host().lower()
        if host in self._exact or host.endswith(self._subdomains):
            self.blocked_count += 1
            info.block(True)