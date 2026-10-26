from dataclasses import dataclass, field
from secrets import token_hex
import json
from pathlib import Path
import logging
from datetime import datetime
from functools import partial
from typing import Callable

from profiles import OtusProfile
from settings import *

from PySide6.QtCore import QObject, Signal
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest

log = logging.getLogger(__name__)

@dataclass
class Download:
    source: str
    filename: str
    timestamp: float
    status: str
    total_bytes: int
    filepath: Path
    received_bytes: int = 0
    ident: str = field(default_factory=lambda: token_hex(4))

    def __post_init__(self):
        self.filepath = Path(self.filepath)

class DownloadManager(QObject):
    downloadUpdated = Signal(Download)
    
    __download_history: list[Download]
    
    def __init__(self, profile: OtusProfile, persistent: bool = True, parent=None):
        super().__init__(parent)
        self.profile = profile
        self.persistent = persistent
        self.__registered_requests: dict[QWebEngineDownloadRequest, Download] = {}
        self.__download_history = self.load() if persistent else []
    
    def load(self) -> list[Download]:
        
        json_file = self.profile.storage_path / "downlad_history.json"
        if not json_file.exists():
            json_file.touch(exist_ok=True)
            return []
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                downloads_data = json.load(f)
                for data in downloads_data:
                    if "filepath" not in data:
                        data["filepath"] = get_download_path() / data["filename"]
                self.__download_history = self.__consolidate_history(
                    [Download(**data) for data in downloads_data]
                )
                self.save()
                return self.__download_history
        except FileNotFoundError:
            log.info("No download history file found, starting with an empty history.")
            self.__download_history = []
            self.save()
            return []
        except Exception as e:
            log.error("Failed to load download history: {error}".format(error=str(e)))
            self.__download_history = []
            self.save()
            return []
        
    def save(self):
        json_file = self.profile.storage_path / "downlad_history.json"
        try:
            downloads_data = [
                {**download.__dict__, "filepath": str(download.filepath)}
                for download in self.__download_history
            ]
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(downloads_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            log.error("Failed to save download history: {error}".format(error=str(e)))
            
    def register(self, request: QWebEngineDownloadRequest):
        existing = self.__registered_requests.get(request)
        if existing is not None:
            self.__update_record(request, existing)
            return existing

        record = Download(
            source=request.url().toString(),
            filename=request.downloadFileName(),  # final name, after unique_path
            filepath=Path(request.downloadDirectory()) / request.downloadFileName(),
            total_bytes=request.totalBytes(),
            status=request.state().name,
            timestamp=datetime.now().timestamp()
        )
        self.__download_history.append(record)
        self.__registered_requests[request] = record
        self.save()

        # Keep the record in sync with the request
        request.receivedBytesChanged.connect(
            partial(self.__on_recieved_bytes_changed, request, record)
        )
        request.stateChanged.connect(
            partial(self.__on_state_changed, request, record)
        )
        request.isFinishedChanged.connect(
            partial(self.__on_finished_changed, request, record)
        )
        return record
        
    def remove(self, record: Download, refresh_callback: Callable[[], None] | None = None):
        self.__download_history = [
            d for d in self.__download_history if d.ident != record.ident
        ]
        self.save()
        if refresh_callback:
            refresh_callback()
            
    def clear_history(self, refresh_callback: Callable[[], None] | None = None):
        self.__download_history.clear()
        self.save()
        if refresh_callback:
            refresh_callback()
        
    def __on_recieved_bytes_changed(
        self, request: QWebEngineDownloadRequest, record: Download, *args
    ):
        self.__update_record(request, record)
        
    def __on_state_changed(
        self, request: QWebEngineDownloadRequest, record: Download, *args
    ):
        self.__update_record(request, record)
        
    def __on_finished_changed(
        self, request: QWebEngineDownloadRequest, record: Download, *args
    ):
        self.__update_record(request, record)

    def __update_record(
        self, request: QWebEngineDownloadRequest, record: Download
    ):
        record.status = request.state().name
        record.total_bytes = request.totalBytes()
        record.received_bytes = request.receivedBytes()
        self.__download_history = [d if d.ident != record.ident else record for d in self.__download_history]
        self.save()
        self.downloadUpdated.emit(record)

    @staticmethod
    def __consolidate_history(downloads: list[Download]) -> list[Download]:
        consolidated: list[Download] = []
        for download in downloads:
            duplicate = next(
                (
                    item
                    for item in consolidated
                    if item.source == download.source
                    and item.filename == download.filename
                    and {
                        item.status,
                        download.status,
                    }
                    <= {"DownloadRequested", "DownloadStarted", "DownloadInProgress"}
                ),
                None,
            )
            if duplicate is None:
                consolidated.append(download)
                continue

            duplicate.status = download.status
            duplicate.total_bytes = download.total_bytes
            duplicate.timestamp = min(duplicate.timestamp, download.timestamp)

        return consolidated
        
    def get_download_history(self) -> list[Download]:
        return self.__download_history.copy()
    
    def count_active_downloads(self) -> int:
        return len([d for d in self.__download_history if d.status in ["DownloadRequested", "DownloadStarted", "DownloadInProgress"]])