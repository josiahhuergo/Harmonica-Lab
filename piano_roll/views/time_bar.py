from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget

from app.state import *
from piano_roll.events import piano_roll_events as events
from piano_roll.colors import Colors
from piano_roll.state import piano_roll_state as state


class TimeBarContent(QWidget):
    """The inner time bar area that gets scrolled around."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(
            state.content_size.width(),
            state.time_bar_height,
        )

    def paintEvent(self, event):
        """Paints the labels and lines for the time bar."""

        painter = QPainter(self)

        painter.setBrush(Colors.BG_BLACK)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())

        for i in range(self.width() // state.beat_width):
            pos = i * state.beat_width

            # Draw lines
            painter.setPen(Colors.BG_WHITE)
            painter.drawLine(
                pos,
                self.height() * (2 / 5),
                pos,
                self.height(),
            )

            # Draw numbers
            painter.setPen(Colors.FG_WHITE)
            painter.drawText(pos + 6, self.height() - 5, str(i))


class TimeBar(QWidget):
    """The scrollable frame that the time bar content sits in."""

    def __init__(self):
        super().__init__()
        self._setup_scroll()
        events.scrolled.connect(self._scroll)
        self.setFixedHeight(state.time_bar_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_scroll_x(self, scroll_x):
        self.scroll_area.horizontalScrollBar().setValue(scroll_x)

    def _scroll(self, scroll_value: QPoint):
        self.set_scroll_x(scroll_value.x())

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
