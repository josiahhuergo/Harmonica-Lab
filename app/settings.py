from dataclasses import dataclass

from PySide6.QtCore import QSize
from PySide6.QtGui import QColor

__all__ = ["settings"]


class Colors:
    def __init__(self):
        self.bg_black_key: QColor = QColor("#212121")
        self.bg_white_key: QColor = QColor("#313131")
        self.fg_black_key: QColor = QColor("#181818")
        self.fg_white_key: QColor = QColor("#8c8c8c")


class Settings:
    def __init__(self):
        self.time_bar_height: int = 30
        self.piano_bar_width: int = 50
        self.zoom_x: float = 1.0 / 2
        self.zoom_y: float = 3.0

        self.black_keys = [1, 3, 6, 8, 10]

        self.content_size: QSize = QSize(2000, 2000)

        self.colors: Colors = Colors()

    @property
    def beat_width(self) -> int:
        return int(30 * self.zoom_x)

    @property
    def key_height(self) -> int:
        return int(20 * self.zoom_y)


settings = Settings()
