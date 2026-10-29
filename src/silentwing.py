from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEngineUrlRequestInfo

from utils import clean_url


RT = QWebEngineUrlRequestInfo.ResourceType
THIRD_PARTY_BLOCKED_TYPES = frozenset({
    RT.ResourceTypeScript,
    RT.ResourceTypeSubFrame,
    RT.ResourceTypePing,
    RT.ResourceTypeCspReport,
    RT.ResourceTypePrefetch,
})
LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
SECOND_LEVEL_LABELS = frozenset({"co", "com", "org", "net", "gov", "ac", "edu"})


def _site(host: str) -> str:
    """Return a rough registrable domain without a Public Suffix List."""
    labels = [label for label in host.split(".") if label]
    if len(labels) >= 3 and labels[-2] in SECOND_LEVEL_LABELS and len(labels[-1]) == 2:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:]) if len(labels) >= 2 else host


class SilentWing:
    """Applies the network part of the SilentWing privacy policy."""

    def __init__(self) -> None:
        self.enabled = False
        self.blocked_count = 0

    def apply(
        self,
        info: QWebEngineUrlRequestInfo,
        url: QUrl,
        host: str,
    ) -> bool:
        """Redirect or block a request according to SilentWing rules."""
        if (
            url.scheme() == "http"
            and host not in LOCAL_HOSTS
            and url.port() == -1
        ):
            secure_url = QUrl(url)
            secure_url.setScheme("https")
            info.redirect(secure_url)
            return True

        if info.resourceType() == RT.ResourceTypeMainFrame:
            cleaned_url = clean_url(url)
            if cleaned_url != url:
                info.redirect(cleaned_url)
                return True
            return False

        first_party_host = info.firstPartyUrl().host().lower()
        if (
            first_party_host
            and info.resourceType() in THIRD_PARTY_BLOCKED_TYPES
            and _site(host) != _site(first_party_host)
        ):
            self.blocked_count += 1
            info.block(True)
            return True

        return False