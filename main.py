import sys

from PySide6.QtWidgets import QApplication

from piano_roll.piano_roll import PianoRoll


def main():
    app = QApplication(sys.argv)
    piano_roll = PianoRoll()
    piano_roll.view.show()
    app.exec()


if __name__ == "__main__":
    main()
