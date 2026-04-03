from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtCore import QSize

from app.piano_roll.notes_area import NotesArea
from app.piano_roll.piano_bar import PianoBar
from app.piano_roll.time_bar import TimeBar


class PianoRoll(QWidget):
    def __init__(self):
        super().__init__()

        self.settings = {
            "time_bar_height": 50,
            "piano_bar_width": 50,
            "content_size": QSize(2000, 2000),
        }

        self.time_bar = TimeBar(self)
        self.piano_bar = PianoBar(self)
        self.notes_area = NotesArea()
        self.corner = QWidget()

        self.corner.setFixedSize(
            QSize(self.settings["piano_bar_width"], self.settings["time_bar_height"])
        )

        self._setup_layout()

    def _setup_layout(self):
        top_hbox = QHBoxLayout()
        top_hbox.setContentsMargins(0, 0, 0, 0)
        top_hbox.setSpacing(0)
        top_hbox.addWidget(self.corner)
        top_hbox.addWidget(self.time_bar)

        bottom_hbox = QHBoxLayout()
        bottom_hbox.setContentsMargins(0, 0, 0, 0)
        bottom_hbox.setSpacing(0)
        bottom_hbox.addWidget(self.piano_bar)
        bottom_hbox.addWidget(self.notes_area)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(top_hbox)
        layout.addLayout(bottom_hbox)

        self.setLayout(layout)
