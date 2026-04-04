from PySide6.QtCore import QRect, Qt
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget
from PySide6.QtGui import QPainter, QColor


class NotesAreaContent(QWidget):
    """Area that can be scrolled around."""

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setFixedSize(settings["content_size"])

    def paintEvent(self, event):
        painter = QPainter(self)
        black_keys = [1, 3, 6, 8, 10]
        colors = self.settings["colors"]

        # Paint note lanes
        key_height = self.settings["key_height"]
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(self.height() // key_height):
            if (i % 12) in black_keys:
                painter.setBrush(QColor(colors["bg_black_key"]))
            else:
                painter.setBrush(QColor(colors["bg_white_key"]))
            painter.drawRect(0, key_height * i, self.width(), key_height)

        # Paint time lines (beats, bars)
        beat_width = self.settings["beat_width"]
        zoom = 4
        painter.setPen(colors["bg_black_key"])
        for i in range(self.width() // beat_width):
            painter.drawLine(
                i * beat_width * zoom, 0, i * beat_width * zoom, self.height()
            )


class NotesArea(QWidget):
    """Frame for the notes area."""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self._setup_scroll()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def _setup_scroll(self):
        scroll_area = QScrollArea()
        self.scroll_area = scroll_area
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)

        content = NotesAreaContent(self.parent.settings)
        scroll_area.setWidget(content)

        layout = QHBoxLayout()
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
