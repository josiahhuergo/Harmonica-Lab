from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QSizePolicy, QWidget


class TimeBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(parent.settings["time_bar_height"])
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("green"))
