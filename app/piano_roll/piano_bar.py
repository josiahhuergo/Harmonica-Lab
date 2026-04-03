from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QSizePolicy, QWidget


class PianoBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedWidth(parent.settings["piano_bar_width"])
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("red"))
