from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QPainter, QShortcut, QShowEvent, QWheelEvent
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout, QWidget

from piano_roll.colors import Colors
from piano_roll.constants import piano_bar_width, time_bar_height
from piano_roll.view.notes import NotesView
from piano_roll.view.piano_bar import PianoBar
from piano_roll.view.scroll_bars import ScrollBarX, ScrollBarY
from piano_roll.view.time_bar import TimeBar
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport
from piano_roll.view.zoom_buttons import ZoomXButtons, ZoomYButtons


class PianoRollFrame(QWidget):
    def __init__(self, vm: PianoRollViewModel):
        super().__init__()
        self.viewport = PianoRollViewport(vm)

        self.time_bar = TimeBar(vm, self.viewport)
        self.piano_bar = PianoBar(vm, self.viewport)
        self.notes_area = NotesView(vm, self.viewport)

        self.scroll_bar_x = ScrollBarX(self.viewport)
        self.scroll_bar_y = ScrollBarY(self.viewport)
        self.zoom_x_buttons = ZoomXButtons(self.viewport)
        self.zoom_y_buttons = ZoomYButtons(self.viewport)

        self._init_layout()
        self._set_bg()
        self._setup_shortcuts()

        self.setFixedSize(1024, 720)

    def _init_layout(self):
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)

        grid.addWidget(self.time_bar, 0, 1)
        grid.addWidget(self.piano_bar, 1, 0)
        grid.addWidget(self.notes_area, 1, 1)
        grid.addWidget(self.scroll_bar_x, 2, 1)
        grid.addWidget(self.scroll_bar_y, 1, 2)
        grid.addWidget(self.zoom_x_buttons, 2, 0)
        grid.addWidget(self.zoom_y_buttons, 0, 2)

        self.setLayout(grid)

    def _set_bg(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Colors.BG_BLACK)
        self.setPalette(palette)

    def _setup_shortcuts(self):
        # Zoom in X: Shift+Z
        zoom_in_shortcut = QShortcut(QKeySequence("Shift+Z"), self)
        zoom_in_shortcut.activated.connect(self.viewport.zoom_in_x)

        # Zoom out X: Shift+X
        zoom_out_shortcut = QShortcut(QKeySequence("Shift+X"), self)
        zoom_out_shortcut.activated.connect(self.viewport.zoom_out_x)

        # Zoom in Y: Ctrl+Shift+Z
        zoom_in_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Z"), self)
        zoom_in_shortcut.activated.connect(self.viewport.zoom_in_y)

        # Zoom out Y: Ctrl+Shift+X
        zoom_out_shortcut = QShortcut(QKeySequence("Ctrl+Shift+X"), self)
        zoom_out_shortcut.activated.connect(self.viewport.zoom_out_x)

    def showEvent(self, event: QShowEvent):
        self.viewport.scroll_to_middle_c()

    def wheelEvent(self, event: QWheelEvent):
        pixel = event.pixelDelta()
        angle = event.angleDelta()

        if not pixel.isNull():
            dx = pixel.x()
            dy = pixel.y()
        else:
            dx = angle.x() // 8
            dy = angle.y() // 8

        self.viewport.adjust_scroll_x(dx)
        self.viewport.adjust_scroll_y(dy)
