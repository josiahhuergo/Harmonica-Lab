from PySide6.QtCore import QObject

from helper import clamp


class PianoRollViewModel(QObject):
    def __init__(self):
        self.max_pitch: int = 108
        self.min_pitch: int = 21

    @property
    def key_count(self) -> int:
        return self.max_pitch - self.min_pitch + 1
