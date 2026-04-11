from PySide6.QtWidgets import QWidget

from piano_roll.views.viewmodel import PianoRollViewModel


class NotesArea(QWidget):
    def __init__(self, vm: PianoRollViewModel):
        self._vm = vm
