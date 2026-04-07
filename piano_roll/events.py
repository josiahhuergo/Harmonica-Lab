from PySide6.QtCore import QObject, QPoint, QSize, Signal


class PianoRollEvents(QObject):
    resized = Signal(QSize)
    scrolled = Signal(QPoint)


piano_roll_events = PianoRollEvents()
