from piano_roll.view.piano_roll_frame import PianoRollFrame
from piano_roll.view.viewmodel import PianoRollViewModel


class PianoRoll:
    def __init__(self):
        self.vm = PianoRollViewModel()
        self.view = PianoRollFrame(self.vm)

    def show(self):
        self.view.show()
