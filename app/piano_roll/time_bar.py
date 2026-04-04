from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget


class TimeBarContent(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.colors = settings["colors"]
        self.settings = settings
        self.setFixedSize(
            settings["content_size"].width(),
            settings["time_bar_height"],
        )

    def paintEvent(self, event):
        painter = QPainter(self)

        # draw lines
        beat_width = self.settings["beat_width"]
        zoom = 4
        painter.setPen(self.colors["bg_black_key"])
        for i in range(self.width() // beat_width):
            painter.drawLine(
                i * beat_width * zoom,
                self.height() / 3,
                i * beat_width * zoom,
                self.height(),
            )


class TimeBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._setup_scroll()
        self.setFixedHeight(parent.settings["time_bar_height"])
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_scroll_x(self, scroll_x):
        self.scroll_area.horizontalScrollBar().setValue(scroll_x)

    def _setup_scroll(self):
        scroll_area = QScrollArea()
        self.scroll_area = scroll_area
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = TimeBarContent(self.parent.settings)
        scroll_area.setWidget(content)

        layout = QHBoxLayout()
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
