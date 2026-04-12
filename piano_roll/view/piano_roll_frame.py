from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QPainter, QShortcut, QWheelEvent
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from piano_roll.colors import Colors
from piano_roll.constants import piano_bar_width, time_bar_height
from piano_roll.view.notes import NotesView
from piano_roll.view.piano_bar import PianoBar
from piano_roll.view.scroll_bars import ScrollBarX, ScrollBarY
from piano_roll.view.time_bar import TimeBar
from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class Corner(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(piano_bar_width, time_bar_height)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(Colors.BG_BLACK)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, piano_bar_width, time_bar_height)


class PianoRollFrame(QWidget):
    def __init__(self, vm: PianoRollViewModel):
        super().__init__()
        self.viewport = PianoRollViewport(vm)

        self.corner = Corner()
        self.time_bar = TimeBar(vm, self.viewport)
        self.piano_bar = PianoBar(vm, self.viewport)
        self.notes_area = NotesView(vm, self.viewport)
        self.scroll_bar_x = ScrollBarX(vm, self.viewport)
        self.scroll_bar_y = ScrollBarY(vm, self.viewport)

        self._init_layout()
        self._setup_shortcuts()

        self.setFixedSize(1024, 720)

    def _init_layout(self):
        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_bar.setSpacing(0)
        top_bar.addWidget(self.corner)
        top_bar.addWidget(self.time_bar)

        bottom_bar = QHBoxLayout()
        bottom_bar.setContentsMargins(0, 0, 0, 0)
        bottom_bar.setSpacing(0)
        bottom_bar.addWidget(self.piano_bar)
        bottom_bar.addWidget(self.notes_area)

        inner_area = QVBoxLayout()
        inner_area.setContentsMargins(0, 0, 0, 0)
        inner_area.setSpacing(0)
        inner_area.addLayout(top_bar)
        inner_area.addLayout(bottom_bar)
        inner_area.addWidget(self.scroll_bar_x)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(inner_area)
        layout.addWidget(self.scroll_bar_y)

        self.setLayout(layout)

    def _setup_shortcuts(self):
        # Zoom in: Shift+Z
        zoom_in_shortcut = QShortcut(QKeySequence("Shift+Z"), self)
        zoom_in_shortcut.activated.connect(self.viewport.zoom_in_x)

        # Zoom out: Shift+X
        zoom_out_shortcut = QShortcut(QKeySequence("Shift+X"), self)
        zoom_out_shortcut.activated.connect(self.viewport.zoom_out_x)

    def wheelEvent(self, event: QWheelEvent):
        dx = event.angleDelta().x()
        dy = event.angleDelta().y()

        self.viewport.adjust_scroll_x(dx)
        self.viewport.adjust_scroll_y(dy)
