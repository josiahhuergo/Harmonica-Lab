from PySide6.QtCore import QObject, QPoint, QSize, Signal

from helper import clamp
from piano_roll.events import piano_roll_events as events


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
        self.view_size: QSize = QSize()

        events.resized.connect(self.resize)

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

    @property
    def notes_area_size(self) -> QSize:
        return QSize()

    @property
    def max_scroll_x(self) -> int:
        return self.content_size.width() - self.view_size.width()

    @property
    def max_scroll_y(self) -> int:
        return self.content_size.height() - self.view_size.height()

    def resize(self, size: QSize):
        self._size = size

    def scroll(self, delta: tuple[int, int]):
        dx, dy = delta

        self.scroll_x = clamp(self.scroll_x - dx, 0, self.max_scroll_x)
        self.scroll_y = clamp(self.scroll_y - dy, 0, self.max_scroll_y)

        events.scrolled.emit(QPoint(self.scroll_x, self.scroll_y))


piano_roll_state = PianoRollState()
