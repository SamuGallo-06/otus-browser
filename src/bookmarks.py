from dataclasses import dataclass, field
import json
import logging
import hashlib
from gettext import gettext as gtr
from pathlib import Path
from PySide6.QtGui import QIcon

from profiles import OtusProfile

from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)

@dataclass
class Bookmark():
    """_summary_
    Properties:
     - url: the URL of the bookmark, used also as a unique identifier for the bookmark
     - title: the title of the bookmark
     - parent: the bookmark parent folder. if is None, it's a root-level bookmark
     - desc: the description of the bookmark
    """
    url: str = field()
    title: str = field()
    parent: str | None = field(default=None)
    desc: str = field(default="")
    
    def __str__(self):
        return f"Bookmark(title={self.title}, url={self.url}, parent={self.parent}, desc={self.desc})"
    
class BookmarkManager(QObject):
    
    reloadRequired = Signal()
    
    def __init__(self, profile: OtusProfile, persistent: bool = True):
        super().__init__()
        self.profile = profile
        self.persistent = persistent
        self.bookmarks_file = self.profile.storage_path / "bookmarks.json"
        self.bookmarks: list[Bookmark] = self.load_bookmarks()
        
    def load_bookmarks(self) -> list[Bookmark]:
        if not self.bookmarks_file.exists():
            self.bookmarks_file.touch(exist_ok=True)
            return []
        try:
            with open(self.bookmarks_file, "r", encoding="utf-8") as f:
                bookmarks_data = json.load(f)
                return [Bookmark(**data) for data in bookmarks_data]
        except Exception as e:
            logger.error(gtr("Failed to load bookmarks: %s"), e)
            return []
        
    def save_bookmarks(self):
        try:
            with open(self.bookmarks_file, "w", encoding="utf-8") as f:
                json.dump([bookmark.__dict__ for bookmark in self.bookmarks], f, ensure_ascii=False, indent=4)
            self.reloadRequired.emit()
        except Exception as e:
            logger.error(gtr("Failed to save bookmarks: %s"), e)
            
    def search(self, url: str) -> Bookmark | None:
        for b in self.bookmarks:
            if b.url == url:
                return b
        return None
    
    def has_bookmark(self, url) -> bool:
        return self.search(url) is not None
    
    def add_bookmark(self, bookmark: Bookmark):
        if not bookmark.url or not bookmark.title:
            logger.error(gtr("Bookmark must have a URL and a title."))
            return
        if any(b.url == bookmark.url for b in self.bookmarks):
            logger.warning(
                gtr("Bookmark with URL '%s' already exists. Skipping addition."),
                bookmark.url,
            )
            return
        print(gtr("Adding bookmark: {bookmark}").format(bookmark=bookmark))
        self.bookmarks.append(bookmark)
        if self.persistent:
            self.save_bookmarks()
        else:
            self.reloadRequired.emit()
        
    def deleteBookmark(self, bookmark: Bookmark):
        print(gtr("Deleting bookmark: {bookmark}").format(bookmark=bookmark))
        self.bookmarks[:] = [b for b in self.bookmarks if b.url != bookmark.url]
        if self.persistent:
            self.save_bookmarks()
        else:
            self.reloadRequired.emit()
        self._icon_file(bookmark.url).unlink(missing_ok=True)
        
    def get_folders(self):
        """Return a list of unique folder names from the bookmarks."""
        return list(set(b.parent for b in self.bookmarks if b.parent is not None))

    def _icon_file(self, url: str) -> Path:
        digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
        return self.profile.storage_path / "favicons" / f"{digest}.png"

    def save_icon(self, url: str, icon: QIcon) -> None:
        """Store the page favicon next to the bookmark (persistent profiles only)."""
        if not self.persistent or icon.isNull():
            return
        path = self._icon_file(url)
        path.parent.mkdir(parents=True, exist_ok=True)
        icon.pixmap(64, 64).save(str(path), "PNG")

    def icon_for(self, url: str) -> QIcon:
        path = self._icon_file(url)
        return QIcon(str(path)) if path.exists() else QIcon()