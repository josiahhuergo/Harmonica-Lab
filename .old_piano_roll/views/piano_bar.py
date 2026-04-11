from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget

from app.state import *
from piano_roll.colors import Colors
from piano_roll.events import piano_roll_events as events
from piano_roll.constants import black_keys
from piano_roll.helper import pitch_to_y
from piano_roll.state import piano_roll_state as state


class PianoBarContent(QWidget):
    """The inner piano bar area that gets scrolled around."""

    def __init__(self):
        super().__init__()

        self.setFixedSize(
            state.piano_bar_width,
            state.content_size.height(),
        )

    def paintEvent(self, event):
        """Paints the piano keys on the left of the piano roll."""

        painter = QPainter(self)

        for p in range(state.max_pitch, state.min_pitch - 1, -1):
            y = pitch_to_y(p)

            if p % 12 in black_keys:
                painter.setBrush(Colors.FG_BLACK)
            else:
                painter.setBrush(Colors.FG_WHITE)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(0, y, self.width(), state.key_height)

            if p % 12 in [4, 11]:
                painter.setPen(Colors.BG_BLACK)
                painter.drawLine(0, y, self.width(), y)
                painter.setPen(Qt.PenStyle.NoPen)


class PianoBar(QWidget):
    """The frame that the scrollable piano bar sits in."""

    def __init__(self):
        super().__init__()
        self._setup_scroll()
        events.scrolled.connect(self._scroll)
        self.setFixedWidth(state.piano_bar_width)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    def set_scroll_y(self, scroll_y):
        self.scroll_area.verticalScrollBar().setValue(scroll_y)

    def _scroll(self, scroll_value: QPoint):
        self.set_scroll_y(scroll_value.y())

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
