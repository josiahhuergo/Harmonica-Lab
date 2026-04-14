import numpy as np
from PySide6.QtCore import QObject, Signal


# Structured dtype for notes. One row = one note.
# Kept as module-level so renderers can reference it.
NOTE_DTYPE = np.dtype(
    [
        ("start", np.float32),  # beat
        ("duration", np.float32),  # beats
        ("pitch", np.int16),  # MIDI pitch
        ("velocity", np.uint8),  # 0..127
    ]
)


def _demo_notes() -> np.ndarray:
    """5,000 random notes spread across pitches and time.

    Deterministic via a fixed seed so visuals are reproducible between runs.
    """
    rng = np.random.default_rng(seed=42)
    n = 1000

    notes = np.empty(n, dtype=NOTE_DTYPE)
    notes["start"] = rng.uniform(0.0, 200.0, size=n)  # 200 beats wide
    notes["duration"] = rng.uniform(0.25, 2.0, size=n)  # eighth to half
    notes["pitch"] = rng.integers(24, 102, size=n, endpoint=True)  # C2..C7
    notes["velocity"] = rng.integers(40, 127, size=n, endpoint=True, dtype=np.uint8)
    return notes


class PianoRollViewModel(QObject):
    notes_changed = Signal()

    def __init__(self):
        super().__init__()
        self.max_pitch: int = 108
        self.min_pitch: int = 21

        self._notes: np.ndarray = _demo_notes()

    @property
    def key_count(self) -> int:
        return self.max_pitch - self.min_pitch + 1

    @property
    def notes(self) -> np.ndarray:
        """Read-only view of the notes array.

        Treat as immutable — to modify, call set_notes with a new array.
        This keeps the signal contract simple: the array reference changes
        iff notes_changed fires.
        """
        return self._notes

    def set_notes(self, notes: np.ndarray):
        if notes.dtype != NOTE_DTYPE:
            raise TypeError(f"notes must have dtype {NOTE_DTYPE}, got {notes.dtype}")
        self._notes = notes
        self.notes_changed.emit()
