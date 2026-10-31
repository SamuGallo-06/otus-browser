import subprocess
import platform
import os

from PySide6.QtWidgets import QBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

from custom.download_view_item import DownloadViewItem
from downloads import Download, DownloadManager
from utils import open_file

from ui.ui_download_manager import Ui_DownloadHistory