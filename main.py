import sys

from PySide6.QtWidgets import QApplication

from app.app import HarmonicaLab


def main():
    app = QApplication(sys.argv)
    lab = HarmonicaLab()
    lab.show()
    app.exec()


if __name__ == "__main__":
    main()
