from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QLabel, QSizePolicy


class ElidedLabel(QLabel):
    """Label that shortens its text to fit the available width."""

    def __init__(self, text: str = "", parent=None,
                 mode: Qt.TextElideMode = Qt.TextElideMode.ElideMiddle):
        super().__init__(parent)
        self._full_text = ""
        self._mode = mode
        self.setTextFormat(Qt.TextFormat.PlainText)
        # Ignored: the label's text length must not force the window to grow
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.set_full_text(text)

    def set_full_text(self, text: str):
        self._full_text = text
        self.setToolTip(text)  # the complete text stays available on hover
        self._update_elided()

    def full_text(self) -> str:
        return self._full_text

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_elided()

    def minimumSizeHint(self) -> QSize:
        # Allow the label to shrink below the width of its text
        return QSize(0, super().minimumSizeHint().height())

    def _update_elided(self):
        width = self.contentsRect().width()
        elided = self.fontMetrics().elidedText(self._full_text, self._mode, width)
        super().setText(elided)