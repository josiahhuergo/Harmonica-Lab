from PySide6.QtCore import QObject, QPoint, QSize, Signal


class PianoRollEvents(QObject):
    resized = Signal(QSize)
    scrolled = Signal(QPoint)
    zoomed_x = Signal(float)
    zoomed_y = Signal(float)


piano_roll_events = PianoRollEvents()
