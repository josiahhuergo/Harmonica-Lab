from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QScrollBar

from piano_roll.constants import scroll_bar_thickness
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class ScrollBarX(QScrollBar):
    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__(Qt.Orientation.Horizontal)

        self.viewport = viewport

        self.setFixedHeight(scroll_bar_thickness)

        self.valueChanged.connect(viewport.set_scroll_x)
        viewport.scrolled.connect(self.update_scroll)
        viewport.resized.connect(self.update_size)

    def update_scroll(self):
        self.setValue(self.viewport.scroll_x)

    def update_size(self):
        self.setRange(0, self.viewport.max_scroll_x)
        self.setPageStep(self.viewport.viewport_height)


class ScrollBarY(QScrollBar):
    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__(Qt.Orientation.Vertical)

        self.viewport = viewport

        self.setFixedWidth(scroll_bar_thickness)

        self.valueChanged.connect(viewport.set_scroll_y)
        viewport.scrolled.connect(self.update_scroll)
        viewport.resized.connect(self.update_size)

    def update_scroll(self):
        self.setValue(self.viewport.scroll_y)

    def update_size(self):
        self.setRange(0, self.viewport.max_scroll_y)
        self.setPageStep(self.viewport.viewport_width)
