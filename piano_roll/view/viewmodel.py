from dataclasses import dataclass
from random import randint

from PySide6.QtCore import QObject, Signal

from harmonica import Mixed
from piano_roll.helper import IDGen, quantize


@dataclass(slots=True)
class NoteData:
    pitch: int
    onset: Mixed
    duration: Mixed


class PianoRollViewModel(QObject):
    notes_changed = Signal()
    selection_changed = Signal()

    def __init__(self):
        super().__init__()
        self.max_pitch: int = 108
        self.min_pitch: int = 21

        self.id_gen: IDGen = IDGen()
        self.notes: dict[int, NoteData] = {}
        self.clipboard: list[NoteData] = []
        self.selected: set[int] = set()

        self.quantize: Mixed = Mixed("1/4")

        # DEBUGGING STUFF #
        notes = [
            NoteData(randint(40, 80), Mixed(i), Mixed("1/4") * randint(1, 8))
            for i in range(100)
        ]
        self.create_notes(notes)

    @property
    def key_count(self) -> int:
        return self.max_pitch - self.min_pitch + 1

    def create_note(self, pitch: int, onset: Mixed, duration: Mixed):
        note = NoteData(pitch, onset, duration)
        id = self.id_gen.get()
        self.notes[id] = note
        self.notes_changed.emit()

    def create_notes(self, notes: list[NoteData]):
        for note in notes:
            id = self.id_gen.get()
            self.notes[id] = note
        self.notes_changed.emit()

    def duplicate_notes(self):
        pass

    def remove_selected(self):
        for sel_id in self.selected:
            del self.notes[sel_id]
            self.id_gen.free(sel_id)
        self.selected = set()
        self.notes_changed.emit()

    def select_note(self, id: int):
        assert id in self.notes.keys(), "id must belong to existing note"
        self.selected.add(id)
        self.selection_changed.emit()

    def select_notes(self, ids: list[int]):
        assert all(
            id in self.notes.keys() for id in ids
        ), "ids must belong to existing notes"
        for id in ids:
            self.selected.add(id)
        self.selection_changed.emit()

    def deselect_note(self, id: int):
        assert id in self.selected, "id must belong to selected note"
        self.selected.remove(id)
        self.selection_changed.emit()

    def deselect_notes(self, ids: list[int]):
        assert all(
            id in self.selected for id in ids
        ), "ids must belong to selected notes"
        for id in ids:
            self.selected.remove(id)
        self.selection_changed.emit()

    def copy_notes(self):
        self.clipboard = [self.notes[id] for id in self.selected]

    def adjust_note_durs(self, delta: Mixed):
        delta = quantize(delta, self.quantize)

        for sel_id in self.selected:
            dur = self.notes[sel_id].duration
            dur = max(dur + delta, self.quantize)
            self.notes[sel_id].duration = dur

        self.notes_changed.emit()
