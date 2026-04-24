from math import ceil

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QSizePolicy, QWidget

from piano_roll.colors import Colors
from piano_roll.constants import time_bar_height
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class TimeBar(QWidget):
    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__()
        self.vm = vm
        self.viewport = viewport

        self.setFixedHeight(time_bar_height)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.viewport.scrolled.connect(self.update)
        self.viewport.zoomed.connect(self.update)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(Colors.BG_BLACK)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())

        beat_width = self.viewport.beat_width
        scroll_x = self.viewport.scroll_x
        scroll_x_in_beats = scroll_x / beat_width
        vp_width = self.viewport.viewport_width
        width = vp_width / beat_width

        start_beat = ceil(scroll_x_in_beats) - 1
        stop_beat = ceil(scroll_x_in_beats + width)

        # Set font size
        font = painter.font()
        font.setPointSize(7)
        painter.setFont(font)

        for i in range(start_beat, stop_beat):
            x = i * beat_width - scroll_x

            line_height = time_bar_height - 5

            if i % 4 == 0:
                line_height = int(time_bar_height * (3 / 7))

            # Draw lines
            painter.setPen(Colors.BG_WHITE)
            painter.drawLine(
                x,
                line_height,
                x,
                time_bar_height,
            )

            # Draw numbers
            if i % 4 == 0:
                painter.setPen(Colors.FG_WHITE)
                painter.drawText(x + 6, self.height() - 8, str(i))
