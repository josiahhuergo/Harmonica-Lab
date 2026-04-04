from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget

from app import settings

colors = settings.colors


class TimeBarContent(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(
            settings.content_size.width(),
            settings.time_bar_height,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        beat_width = settings.beat_width

        for i in range(self.width() // beat_width):
            pos = i * beat_width

            # Draw lines
            painter.setPen(colors.bg_black_key)
            painter.drawLine(
                pos,
                self.height() / 2,
                pos,
                self.height(),
            )

            # Draw numbers
            painter.setPen(colors.fg_white_key)
            painter.drawText(pos + (beat_width / 4), self.height() - 5, str(i + 1))


class TimeBar(QWidget):
    def __init__(self):
        super().__init__()
        self._setup_scroll()
        self.setFixedHeight(settings.time_bar_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_scroll_x(self, scroll_x):
        self.scroll_area.horizontalScrollBar().setValue(scroll_x)

    def _setup_scroll(self):
        scroll_area = QScrollArea()
        self.scroll_area = scroll_area
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = TimeBarContent()
        scroll_area.setWidget(content)

        layout = QHBoxLayout()
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
