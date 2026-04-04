from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget


class PianoBarContent(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.colors = settings["colors"]
        self.setFixedSize(
            settings["piano_bar_width"],
            settings["content_size"].height(),
        )

    def paintEvent(self, event):
        painter = QPainter(self)


class PianoBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self._setup_scroll()

        self.setFixedWidth(parent.settings["piano_bar_width"])
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    def set_scroll_y(self, scroll_y):
        self.scroll_area.verticalScrollBar().setValue(scroll_y)

    def _setup_scroll(self):
        scroll_area = QScrollArea()
        self.scroll_area = scroll_area
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = PianoBarContent(self.parent.settings)
        scroll_area.setWidget(content)

        layout = QHBoxLayout()
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
