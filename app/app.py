from PySide6.QtWidgets import QMainWindow

from PySide6.QtCore import Qt

from app.state import app_state as state
from piano_roll.widgets.piano_roll import PianoRoll


class HarmonicaLab(QMainWindow):
    def __init__(self):
        super().__init__()
        self.piano_roll = PianoRoll()
        self.setCentralWidget(self.piano_roll)
        self.setWindowTitle("Harmonica Lab")
        self.setMinimumSize(state.window_size)

    def keyPressEvent(self, event):
        # Close app if ESC is pressed
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        super().keyPressEvent(event)
