from math import floor

from PySide6.QtCore import QObject, Signal

from helper import clamp
from piano_roll.view.viewmodel import PianoRollViewModel


class PianoRollViewport(QObject):
    """State and behavior specific to the viewport, such as scrolling
    and zooming."""

    scrolled = Signal()
    zoomed = Signal()
    resized = Signal()

    _DEFAULT_BEAT_WIDTH = 50
    _DEFAULT_KEY_HEIGHT = 18
    _ZOOM_FACTOR = 1.5
    _ZOOM_X_MIN = 0.1
    _ZOOM_X_MAX = 4.0
    _ZOOM_Y_MIN = 0.25
    _ZOOM_Y_MAX = 2.0
    _SCROLL_SPEED = 0.8

    def __init__(self, vm: PianoRollViewModel):
        super().__init__()
        self.vm = vm  # Only for reading

        self.scroll_x: float = 0  # Scroll position (in pixels)
        self.scroll_y: float = 0
        self.zoom_x: float = 1.0  # Zoom multipliers
        self.zoom_y: float = 1.0
        self.viewport_size: tuple[int, int] = (0, 0)

    @property
    def content_width(self) -> int:
        return 2500

    @property
    def content_height(self) -> int:
        return int(self.vm.key_count * self.key_height)

    @property
    def viewport_width(self) -> int:
        return self.viewport_size[0]

    @property
    def viewport_height(self) -> int:
        return self.viewport_size[1]

    @property
    def beat_width(self) -> float:
        return self._DEFAULT_BEAT_WIDTH * self.zoom_x

    @property
    def key_height(self) -> float:
        return self._DEFAULT_KEY_HEIGHT * self.zoom_y

    @property
    def max_scroll_x(self) -> int:
        return self.content_width - self.viewport_width

    @property
    def max_scroll_y(self) -> int:
        return self.content_height - self.viewport_height

    def set_viewport_size(self, new_size: tuple[float, float]):
        self.viewport_size = new_size
        self.resized.emit()

    def set_scroll_x(self, new_scroll_x: int):
        new_scroll_x = clamp(new_scroll_x, 0, self.max_scroll_x)
        self.scroll_x = new_scroll_x
        self.scrolled.emit()

    def set_scroll_y(self, new_scroll_y: int):
        new_scroll_y = clamp(new_scroll_y, 0, self.max_scroll_y)
        self.scroll_y = new_scroll_y
        self.scrolled.emit()

    def set_zoom_x(self, new_zoom_x: float):
        self.zoom_x = clamp(new_zoom_x, self._ZOOM_X_MIN, self._ZOOM_X_MAX)
        self.zoomed.emit()

    def set_zoom_y(self, new_zoom_y: float):
        self.zoom_y = clamp(new_zoom_y, self._ZOOM_Y_MIN, self._ZOOM_Y_MAX)
        self.zoomed.emit()

    def adjust_scroll_x(self, delta: int):
        self.set_scroll_x(self.scroll_x - (delta * self._SCROLL_SPEED))

    def adjust_scroll_y(self, delta: int):
        self.set_scroll_y(self.scroll_y - (delta * self._SCROLL_SPEED))

    def zoom_in_x(self):
        self.set_zoom_x(self.zoom_x * self._ZOOM_FACTOR)

    def zoom_out_x(self):
        self.set_zoom_x(self.zoom_x / self._ZOOM_FACTOR)

    def zoom_in_y(self):
        self.set_zoom_y(self.zoom_y * self._ZOOM_FACTOR)

    def zoom_out_y(self):
        self.set_zoom_y(self.zoom_y / self._ZOOM_FACTOR)

    def scroll_to_middle_c(self):
        y = (self.vm.max_pitch - 60) * self.key_height
        self.set_scroll_y(y - self.viewport_height / 2)

    def _pitch_to_y(self, pitch: int) -> int:
        """Takes a pitch integer and returns the y position of the
        top of the corresponding key lane in the piano roll."""

        return int((self.vm.max_pitch - pitch) * self.key_height) - self.scroll_y

    def _time_to_x(self, beat: float) -> int:
        """Takes a point in time and translates it into a pixel position."""

        return int(self.beat_width * beat) - self.scroll_x

    def _y_to_pitch(self, y: int) -> int:
        """Takes a y position in pixels and returns the pitch of the key
        lane at that position."""

        return int(self.vm.max_pitch - (y / self.key_height))

    def _x_to_time(self, x: int) -> float:
        """Takes an x position in pixels and returns the point in time
        at that position."""

        return x / self.beat_width
