import numpy as np
from PySide6.QtCore import QObject, Signal


class PianoRollViewModel(QObject):
    notes_changed = Signal()

    def __init__(self):
        super().__init__()
        self.max_pitch: int = 108
        self.min_pitch: int = 21

    @property
    def key_count(self) -> int:
        return self.max_pitch - self.min_pitch + 1
