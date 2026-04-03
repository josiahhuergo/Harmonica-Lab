from PySide6.QtWidgets import QMainWindow

from PySide6.QtCore import QSize

from app.piano_roll.piano_roll import PianoRoll


class HarmonicaLab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.piano_roll = PianoRoll()
        self.setCentralWidget(self.piano_roll)
        self.setWindowTitle("HarmonicaLab")
        self.setFixedSize(QSize(1280, 720))
