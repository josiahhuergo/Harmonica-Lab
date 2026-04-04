from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget
from PySide6.QtGui import QPainter, QColor

from app import settings

colors = settings.colors


class NotesAreaContent(QWidget):
    """Area that can be scrolled around."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(settings.content_size)

    def paintEvent(self, event):
        painter = QPainter(self)
        black_keys = settings.black_keys

        # Paint note lanes
        key_height = settings.key_height
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(self.height() // key_height):
            if (i % 12) in black_keys:
                painter.setBrush(colors.bg_black_key)
            else:
                painter.setBrush(colors.bg_white_key)
            painter.drawRect(0, key_height * i, self.width(), key_height)

        # Paint time lines (beats, bars)
        beat_width = settings.beat_width
        painter.setPen(colors.bg_black_key)
        for i in range(self.width() // beat_width):
            painter.drawLine(i * beat_width, 0, i * beat_width, self.height())


class NotesArea(QWidget):
    """Frame for the notes area."""

    def __init__(self):
        super().__init__()
        self._setup_scroll()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _setup_scroll(self):
        scroll_area = QScrollArea()
        self.scroll_area = scroll_area
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = NotesAreaContent()
        scroll_area.setWidget(content)

        layout = QHBoxLayout()
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
