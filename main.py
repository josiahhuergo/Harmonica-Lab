import sys

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import QApplication

from helper import EscapeFilter
from piano_roll.piano_roll import PianoRoll


def main():
    app = QApplication(sys.argv)

    # Enables pressing Esc to quit
    esc_filter = EscapeFilter()
    app.installEventFilter(esc_filter)

    piano_roll = PianoRoll()
    piano_roll.view.setWindowTitle("Harmonica Lab")
    piano_roll.show()
    app.exec()


if __name__ == "__main__":
    main()
