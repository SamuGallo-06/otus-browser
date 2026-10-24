from dataclasses import dataclass, field
from secrets import token_hex
import json
from pathlib import Path
import logging
from datetime import datetime

from profiles import OtusProfile
from settings import *

from PySide6.QtCore import QObject
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest

log = logging.getLogger(__name__)

@dataclass
class Download:
    source: str = field()
    filename: str = field()
    timestamp: float = field()
    status: str = field()
    total_bytes: int = field()
    ident: str = field(default=token_hex(4))

class DownloadManager(QObject):
    
    __download_history: list[Download]
    
    def __init__(self, profile: OtusProfile, persistent:bool = True):
        self.profile = profile
        self.peristent = persistent
        self.__download_history = self.load() if persistent else []
    
    def load(self) -> list[Download]:
        
        json_file = self.profile.storage_path / "downlad_history.json"
        if not json_file.exists():
            json_file.touch(exist_ok=True)
            return []
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                downloads_data = json.load(f)
                self.__download_history = [Download(**data) for data in downloads_data]
                return self.__download_history
        except Exception as e:
            log.error("Failed to load download history: {e}".format(e))
            self.__download_history = []
            return []
        
    def save(self):
        json_file = self.profile.storage_path / "downlad_history.json"
        try:
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump([download.__dict__ for download in self.__download_history], f, ensure_ascii=False, indent=4)
        except Exception as e:
            log.error("Failed to save download history: {e}".format(e))
            
    def register(self, request: QWebEngineDownloadRequest):
        record = Download(
            source=request.url().toString(),
            filename=request.downloadFileName(),  # final name, after unique_path
            total_bytes=request.totalBytes(),
            status=request.state().name,
            timestamp=datetime.now().timestamp()
        )
        self.__download_history.append(record)
        self.save()

        # Keep the record in sync with the request
        request.receivedBytesChanged.connect(self.__on_recieved_bytes_changed(request, record))
        request.stateChanged.connect(self.__on_state_changed(request, record))
        request.isFinishedChanged.connect(self.__on_finished_changed(request, record))
        
    def __on_recieved_bytes_changed(self, request: QWebEngineDownloadRequest, record: Download):
        record.total_bytes = request.totalBytes()
        self.__download_history = [d if d.ident != record.ident else record for d in self.__download_history]
        self.save()
        
    def __on_state_changed(self, request: QWebEngineDownloadRequest, record: Download):
        record.status = request.state().name
        self.__download_history = [d if d.ident != record.ident else record for d in self.__download_history]
        self.save()
        
    def __on_finished_changed(self, request: QWebEngineDownloadRequest, record: Download):
        record.total_bytes = request.totalBytes()
        self.__download_history = [d if d.ident != record.ident else record for d in self.__download_history]
        self.save()
        
    def get_download_history(self) -> list[Download]:
        return self.__download_history.copy()