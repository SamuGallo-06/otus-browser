import sqlite3

from dataclasses import dataclass, field
from pathlib import Path
import time

from PySide6.QtCore import QObject, Signal, Qt

from profiles import OtusProfile

@dataclass(frozen=True)
class HistoryEntry:
    id: int
    url: str
    title: str
    visited_at: float  # Unix timestamp of the last visit
    visit_count: int = 1
    

class HistoryManager(QObject):
    
    onHistoryLoaded = Signal(list)
    historyChanged = Signal()
    
    _COLUMNS = "id, url, title, visited_at, visit_count"
    
    def __init__(self, profile: OtusProfile, persistent: bool = True, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.persistent = persistent
        self.records: list[HistoryEntry] = []

        path = (self.profile.storage_path / "History.sqlite3") if persistent else ":memory:"
        self.__db = sqlite3.connect(path)
        self.__db.row_factory = sqlite3.Row

        self.__db.execute("""CREATE TABLE IF NOT EXISTS History(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL UNIQUE,
            title TEXT NOT NULL,
            visited_at REAL NOT NULL,
            visit_count INTEGER NOT NULL
            )"""
        )
        
        
    def load_history(self) -> list[HistoryEntry]:
        """Load the history from the database."""
        cursor = self.__db.execute(f"SELECT {self._COLUMNS} FROM History ORDER BY visited_at DESC")
        self.records = [HistoryEntry(**row) for row in cursor]
        return self.records
    
    def add_visit(self, url: str, title: str) -> None:
        self.__db.execute(
            """INSERT INTO History (url, title, visited_at, visit_count)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                visited_at = excluded.visited_at,
                visit_count = visit_count + 1""",
            (url, title, time.time()),
        )
        self.__db.commit()

    def search_history(self, text: str, limit: int = 500) -> list[HistoryEntry]:
        like = f"%{text}%"
        cursor = self.__db.execute(
            f"SELECT {self._COLUMNS} FROM History "
            "WHERE url LIKE ? OR title LIKE ? "
            "ORDER BY visited_at DESC LIMIT ?",
            (like, like, limit),
        )
        return [HistoryEntry(**row) for row in cursor]
    
    def delete_entries(self, ids: list[int]) -> None:
        self.__db.executemany(
            "DELETE FROM History WHERE id = ?",
            [(i,) for i in ids],
        )
        self.__db.commit()
        self.historyChanged.emit()

    def clear_since(self, since: float | None = None) -> None:
        # since=None clears everything; otherwise only visits after the timestamp
        
        if since is None:
            self.__db.execute("DELETE FROM History")
        else:
            self.__db.execute("DELETE FROM History WHERE visited_at >= ?", (since,))
            
        self.__db.commit()
        
        if since is None:
            self.__db.execute("VACUUM")
        self.historyChanged.emit()

    def close(self) -> None:
        self.__db.close()     
    