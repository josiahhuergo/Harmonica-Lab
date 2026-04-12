from PySide6.QtCore import QObject, Signal

from helper import clamp
from piano_roll.view.viewmodel import PianoRollViewModel


class PianoRollViewport(QObject):
    """State and behavior specific to the viewport,
    such as scrolling and zooming."""

    scroll_changed = Signal()
    zoom_changed = Signal()
    viewport_size_changed = Signal()

    _DEFAULT_BEAT_WIDTH = 40
    _DEFAULT_KEY_HEIGHT = 15
    _ZOOM_FACTOR = 1.25
    _ZOOM_X_MIN = 0.25
    _ZOOM_X_MAX = 4.0
    _ZOOM_Y_MIN = 0.25
    _ZOOM_Y_MAX = 2.0

    def __init__(self, vm: PianoRollViewModel):
        super().__init__()
        self.vm = vm  # Only for reading

        self.scroll_pos: tuple[int, int] = (
            0,
            0,
        )  # Scroll position in pixels
        self.zoom_x: float = 1.0  # Zoom multipliers
        self.zoom_y: float = 1.0
        self.viewport_size: tuple[int, int] = (360, 240)

    @property
    def content_size(self) -> tuple[int, int]:
        content_width = 2500
        content_height = int(self.vm.key_count * self.key_height)

        return (content_width, content_height)

    @property
    def beat_width(self) -> float:
        return self._DEFAULT_BEAT_WIDTH * self.zoom_x

    @property
    def key_height(self) -> float:
        return self._DEFAULT_KEY_HEIGHT * self.zoom_y

    @property
    def max_scroll(self) -> tuple[int, int]:
        max_scroll_x = self.content_size[0] - self.viewport_size[0]
        max_scroll_y = self.content_size[1] - self.viewport_size[1]

        return (max_scroll_x, max_scroll_y)

    def set_viewport_size(self, new_size: tuple[float, float]):
        self.viewport_size = new_size
        self.viewport_size_changed.emit()

    def scroll(self, delta: tuple[int, int]):
        scroll_x, scroll_y = self.scroll_pos
        delta_x, delta_y = delta
        max_scroll_x, max_scroll_y = self.max_scroll

        new_scroll_pos = (
            clamp(scroll_x - delta_x, 0, max_scroll_x),
            clamp(scroll_y - delta_y, 0, max_scroll_y),
        )

        self.scroll_pos = new_scroll_pos
        self.scroll_changed.emit()

    def zoom_in_x(self):
        self.set_zoom_x(self.zoom_x * self._ZOOM_FACTOR)

    def zoom_out_x(self):
        self.set_zoom_x(self.zoom_x / self._ZOOM_FACTOR)

    def zoom_in_y(self):
        self.set_zoom_y(self.zoom_y * self._ZOOM_FACTOR)

    def zoom_out_y(self):
        self.set_zoom_y(self.zoom_y / self._ZOOM_FACTOR)

    def set_zoom_x(self, new_zoom_x: float):
        """Clamps x zoom value before setting."""
        self.zoom_x = clamp(new_zoom_x, self._ZOOM_X_MIN, self._ZOOM_X_MAX)
        self.zoom_changed.emit()
        print("ZOOM X EMITTED!")

    def set_zoom_y(self, new_zoom_y: float):
        """Clamps y zoom value before setting."""
        self.zoom_y = clamp(new_zoom_y, self._ZOOM_Y_MIN, self._ZOOM_Y_MAX)
        self.zoom_changed.emit()

    def _pitch_to_y(self, pitch: int) -> int:
        """Takes a pitch integer and returns the y position of the
        top of the corresponding key lane in the piano roll."""

        return int((self.vm.max_pitch - pitch) * self.key_height)

    def _time_to_x(self, beat: float) -> int:
        """Takes a point in time and translates it into a pixel position."""

        return int(self.beat_width * beat)

    def _y_to_pitch(self, y: int) -> int:
        """Takes a y position in pixels and returns the pitch of the key
        lane at that position."""

        return int(self.vm.max_pitch - (y / self.key_height))

    def _x_to_time(self, x: int) -> float:
        """Takes an x position in pixels and returns the point in time
        at that position."""

        return x / self.beat_width
