from piano_roll.views.piano_roll_frame import PianoRollFrame
from piano_roll.views.viewmodel import PianoRollViewModel


class PianoRoll:
    def __init__(self):
        self.vm = PianoRollViewModel()
        self.view = PianoRollFrame(self.vm)

    def show(self):
        self.view.show()
