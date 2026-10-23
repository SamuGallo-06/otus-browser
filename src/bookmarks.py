from dataclasses import dataclass, field
import json
import logging

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
        self.bookmarks = self.load_bookmarks()
        
    def load_bookmarks(self):
        if not self.bookmarks_file.exists():
            self.bookmarks_file.touch(exist_ok=True)
            return []
        try:
            with open(self.bookmarks_file, "r", encoding="utf-8") as f:
                bookmarks_data = json.load(f)
                return [Bookmark(**data) for data in bookmarks_data]
        except Exception as e:
            logger.error("Failed to load bookmarks: %s", e)
            return []
        
    def save_bookmarks(self):
        try:
            with open(self.bookmarks_file, "w", encoding="utf-8") as f:
                json.dump([bookmark.__dict__ for bookmark in self.bookmarks], f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error("Failed to save bookmarks: %s", e)
    
    def add_bookmark(self, bookmark: Bookmark):
        print(f"Adding bookmark: {bookmark}")
        self.bookmarks.append(bookmark)
        if self.persistent:
            self.save_bookmarks()
        self.reloadRequired.emit()
        
    def deleteBookmark(self, bookmark: Bookmark):
        print(f"Deleting bookmark: {bookmark}")
        self.bookmarks = [b for b in self.bookmarks if b.url != bookmark.url]
        if self.persistent:
            self.save_bookmarks()
        self.reloadRequired.emit()
        
    def get_folders(self):
        """Return a list of unique folder names from the bookmarks."""
        return list(set(b.parent for b in self.bookmarks if b.parent is not None))