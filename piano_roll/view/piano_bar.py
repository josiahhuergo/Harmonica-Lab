from math import ceil, floor

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QSizePolicy, QWidget

from piano_roll.colors import Colors
from piano_roll.constants import piano_bar_width, black_keys
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class PianoBar(QWidget):
    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__()
        self.vm = vm
        self.viewport = viewport

        self.setFixedWidth(piano_bar_width)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self.viewport.scrolled.connect(self.update)
        self.viewport.zoomed.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)

        # Some variables
        scroll_y = self.viewport.scroll_y
        key_height = self.viewport.key_height
        vp_height = self.viewport.viewport_height
        max_pitch = self.vm.max_pitch

        start_i = floor(scroll_y / key_height)
        stop_i = ceil((scroll_y + vp_height) / key_height)

        x = piano_bar_width / 2

        # Set font size
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)

        for i in range(start_i, stop_i + 1):
            pitch = max_pitch - i
            y = key_height * i - scroll_y

            if pitch % 12 in black_keys:
                painter.setBrush(Colors.FG_BLACK)
            else:
                painter.setBrush(Colors.FG_WHITE)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(x, y, piano_bar_width, key_height)

            if pitch % 12 in [4, 11]:
                painter.setPen(Colors.BG_BLACK)
                painter.drawLine(x, y, self.width(), y)
                painter.setPen(Qt.PenStyle.NoPen)

            if pitch % 12 == 11:
                rect = QRect(0, y - key_height, x, key_height)
                octave = (pitch + 1) // 12 - 1
                painter.setPen(Colors.BG_WHITE)
                painter.drawLine(x / 2, y, x, y)
                painter.setPen(Colors.FG_WHITE)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "C" + str(octave))
                painter.setPen(Qt.PenStyle.NoPen)
