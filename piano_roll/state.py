from PySide6.QtCore import QObject, QSize


class PianoRollState(QObject):
    def __init__(self):
        self.time_bar_height: int = 30
        self.piano_bar_width: int = 50
        self.zoom_x: float = 1.0
        self.zoom_y: float = 1.0
        self.scroll_x: int = 0
        self.scroll_y: int = 0
        self.min_pitch: int = 21
        self.max_pitch: int = 108

    @property
    def beat_width(self) -> int:
        return int(50 * self.zoom_x)

    @property
    def key_height(self) -> int:
        return int(20 * self.zoom_y)

    @property
    def key_count(self) -> int:
        return self.max_pitch - self.min_pitch + 1

    @property
    def content_size(self) -> QSize:
        return QSize(2000, self.key_count * self.key_height)


piano_roll_state = PianoRollState()
