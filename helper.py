from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication


def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))


class EscapeFilter(QObject):
    """Installing this on the application instance lets us
    use the Esc key to quit."""

    def eventFilter(self, obj, event):
        # if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:  # type: ignore
        #     QApplication.quit()
        #     return True  # event handled, don't propagate
        return super().eventFilter(obj, event)
