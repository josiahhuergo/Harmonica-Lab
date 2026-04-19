from piano_roll.view.piano_roll_frame import PianoRollFrame
from piano_roll.view.viewmodel import PianoRollViewModel

import harmonica


class PianoRoll:
    def __init__(self):
        self.clip = harmonica.time
        self.vm = PianoRollViewModel()
        self.view = PianoRollFrame(self.vm)

    def show(self):
        self.view.show()
