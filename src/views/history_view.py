from functools import partial

from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QMessageBox, QPushButton, QTableWidgetItem, QWidget
from PySide6.QtCore import QDate, QDateTime, QTime, QUrl, Qt, Signal
from PySide6.QtGui import QIcon

from datetime import datetime

from history import HistoryManager, HistoryEntry
from ui.ui_history import Ui_HistoryForm
from settings import FEATHER_ICON_PACK
from user_settings import get_app_settings

class HistoryView(QWidget):
    
    openUrlRequested = Signal(QUrl)
    
    def __init__(self, history_manager: HistoryManager, parent=None):
        super().__init__(parent)
        
        self.__history_manager = history_manager
        self.__history_manager.historyChanged.connect(self.refresh_table)
        
        self.ui = Ui_HistoryForm()
        self.setWindowFlag(Qt.WindowType.Window)
        self.ui.setupUi(self)
        header = self.ui.historyTable.horizontalHeader()
        header.setStretchLastSection(False)  # Otherwise the last column also expands
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)           # URL takes the remaining space
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Title
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Visited At
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Visit Count
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Actions
        self.ui.historyTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.historyTable.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.ui.historyTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.historyTable.setSortingEnabled(False)
        
        self.ui.dateEdit.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit.setMaximumDate(QDate.currentDate())
        self.ui.dateEdit.setDate(QDate.currentDate())
        
        self.ui.historyTable.cellDoubleClicked.connect(self.on_cell_double_clicked)
        
        self.ui.deleteAllButton.clicked.connect(self.on_delete_all)
        self.ui.deleteSince.clicked.connect(self.on_delete_since)
        
        self.refresh_table()
        
    def refresh_table(self):
        self.ui.historyTable.setRowCount(0)    
        self.history = self.__history_manager.load_history()
        
        for i, entry in enumerate(self.history):
            visited_at = datetime.fromtimestamp(entry.visited_at).strftime(
                get_app_settings().settings.date_format
            )
        
            self.ui.historyTable.insertRow(i)
            self.ui.historyTable.setItem(i, 0, QTableWidgetItem(entry.url))
            self.ui.historyTable.setItem(i, 1, QTableWidgetItem(entry.title))
            self.ui.historyTable.setItem(i, 2, QTableWidgetItem(visited_at))
            self.ui.historyTable.setItem(i, 3, QTableWidgetItem(str(entry.visit_count)))
            button = QPushButton()
            button.setIcon(QIcon(FEATHER_ICON_PACK + "trash-2.svg"))
            button.clicked.connect(partial(self.on_delete_rows, entry.id))
            self.ui.historyTable.setCellWidget(i, 4, button)
            
    def on_delete_rows(self, _entry_id: int = 0, *_):
        
        rows = {index.row() for index in self.ui.historyTable.selectionModel().selectedRows()}
        if not rows:
            return
        
        self.__history_manager.delete_entries([self.history[r].id for r in rows])
            
    def on_cell_double_clicked(self, row: int, column: int):
        url = ""
        url = self.history[row].url
        self.openUrlRequested.emit(url)
        self.close()
        
    def on_delete_since(self):
        result = QMessageBox.question(
            self,
            "Delete Entire History",
            "Delete the entire history? This cannot be undone."
        )
                
        if result != QMessageBox.StandardButton.Yes:
            return
        
        qdate = self.ui.dateEdit.date()
        ts = float(QDateTime(qdate, QTime(0, 0)).toSecsSinceEpoch())
        
        self.__history_manager.clear_since(ts)
    
    def on_delete_all(self):
        
        result = QMessageBox.question(
            self,
            "Delete Entire History",
            "Delete the entire history? This cannot be undone."
        )
        
        if result != QMessageBox.StandardButton.Yes:
            return
        
        self.__history_manager.clear_since(None)