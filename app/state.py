from PySide6.QtCore import QObject, QSize


class AppState(QObject):
    def __init__(self):
        self.window_size = QSize(640, 480)


app_state = AppState()
