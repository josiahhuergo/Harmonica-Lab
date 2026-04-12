from PySide6.QtGui import Qt
from PySide6.QtWidgets import QScrollBar

from piano_roll.constants import scroll_bar_thickness
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class ScrollBarX(QScrollBar):
    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__(Qt.Orientation.Horizontal)

        self.viewport = viewport

        self.setRange(0, viewport.max_scroll_x)
        self.setFixedHeight(scroll_bar_thickness)

        viewport.scrolled.connect(self.update_scroll)

    def update_scroll(self):
        self.setValue(self.viewport.scroll_x)


class ScrollBarY(QScrollBar):
    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__(Qt.Orientation.Vertical)

        self.viewport = viewport

        self.setRange(0, viewport.max_scroll_y)
        self.setFixedWidth(scroll_bar_thickness)

        viewport.scrolled.connect(self.update_scroll)

    def update_scroll(self):
        self.setValue(self.viewport.scroll_y)
