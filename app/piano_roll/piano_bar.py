from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget

from app import settings

colors = settings.colors


class PianoBarContent(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(
            settings.piano_bar_width,
            settings.content_size.height(),
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        key_height = settings.key_height
        black_keys = settings.black_keys

        for i in range(self.height() // key_height):
            if i % 12 in black_keys:
                painter.setBrush(colors.fg_black_key)
            else:
                painter.setBrush(colors.fg_white_key)
            pos = i * key_height
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(0, pos, self.width(), key_height)


class PianoBar(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_scroll()

        self.setFixedWidth(settings.piano_bar_width)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    def set_scroll_y(self, scroll_y):
        self.scroll_area.verticalScrollBar().setValue(scroll_y)

    def _setup_scroll(self):
        scroll_area = QScrollArea()
        self.scroll_area = scroll_area
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = PianoBarContent()
        scroll_area.setWidget(content)

        layout = QHBoxLayout()
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
