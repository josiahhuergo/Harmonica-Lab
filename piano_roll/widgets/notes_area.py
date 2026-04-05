from copy import deepcopy

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget
from PySide6.QtGui import QPainter

from piano_roll.colors import Colors
from piano_roll.constants import black_keys
from piano_roll.helpers import pitch_to_y
from piano_roll.state import piano_roll_state as state


class NotesAreaContent(QWidget):
    """Area that can be scrolled around."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(state.content_size)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Paint note lanes
        painter.setPen(Qt.PenStyle.NoPen)

        for p in range(state.max_pitch, state.min_pitch - 1, -1):
            y = pitch_to_y(p)

            if (p % 12) in black_keys:
                painter.setBrush(Colors.BG_BLACK)
            else:
                painter.setBrush(Colors.BG_WHITE)

            painter.drawRect(0, y, self.width(), state.key_height)

            if p % 12 in [4, 11]:
                painter.setPen(Colors.BG_BLACK)
                painter.drawLine(0, y, self.width(), y)
                painter.setPen(Qt.PenStyle.NoPen)

        # Paint time lines (beats, bars)
        for p in range(self.width() // state.beat_width):
            if p % 4 == 0:
                painter.setPen(Colors.FG_BLACK)
            else:
                color = deepcopy(Colors.BG_BLACK)
                color.setAlphaF(1 / 2)
                painter.setPen(color)
            painter.drawLine(
                p * state.beat_width, 0, p * state.beat_width, self.height()
            )


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
