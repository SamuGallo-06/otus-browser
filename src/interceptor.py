from collections.abc import Sequence
from typing import Protocol

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtWebEngineCore import (
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)


class RequestPolicy(Protocol):
    enabled: bool

    def apply(
        self,
        info: QWebEngineUrlRequestInfo,
        url: QUrl,
        host: str,
    ) -> bool:
        """Return True when the request was handled."""
        ...


class OtusRequestInterceptor(QWebEngineUrlRequestInterceptor):
    requestBlocked = Signal()

    def __init__(
        self,
        policies: Sequence[RequestPolicy],
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self._policies = tuple(policies)

    def interceptRequest(
        self,
        info: QWebEngineUrlRequestInfo,
    ) -> None:
        url = info.requestUrl()
        if url.scheme() not in {"http", "https"}:
            return

        host = url.host().lower()

        for policy in self._policies:
            if policy.enabled and policy.apply(info, url, host):
                self.requestBlocked.emit()
                return