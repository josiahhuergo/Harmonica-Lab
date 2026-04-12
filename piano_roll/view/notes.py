from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QSizePolicy, QWidget

from piano_roll.view.viewmodel import PianoRollViewModel
from piano_roll.view.viewport import PianoRollViewport


class NotesView(QWidget):
    def __init__(self, vm: PianoRollViewModel, viewport: PianoRollViewport):
        super().__init__()
        self.viewport = viewport
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def resizeEvent(self, event: QResizeEvent):
        self.viewport.set_viewport_size((event.size().width(), event.size().height()))
