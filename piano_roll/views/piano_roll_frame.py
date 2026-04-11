from PySide6.QtWidgets import QWidget

from piano_roll.views.notes_area import NotesArea
from piano_roll.views.piano_bar import PianoBar
from piano_roll.views.time_bar import TimeBar
from piano_roll.views.viewmodel import PianoRollViewModel


class PianoRollFrame(QWidget):
    def __init__(self, vm: PianoRollViewModel):
        self._vm = vm
        self.time_bar = TimeBar()
        self.piano_bar = PianoBar()
        self.notes_area = NotesArea(vm)
