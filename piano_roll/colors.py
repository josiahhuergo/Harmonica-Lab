from PySide6.QtGui import QColor


class Colors:
    BG_BLACK: QColor = QColor("#2A2A2A")
    BG_WHITE: QColor = QColor("#333333")
    BG_WHITE_2: QColor = QColor("#353535")
    FG_BLACK: QColor = QColor("#181818")
    FG_WHITE: QColor = QColor("#8c8c8c")
    BAR_LINE: QColor = QColor("#151515")
    BEAT_LINE: QColor = QColor("#232323")
    NOTE_BODY: QColor = QColor("#350097")


def rgb(color: QColor) -> tuple[float, float, float]:
    return (color.redF(), color.greenF(), color.blueF())


def rgba(color: QColor, alpha: float = 1.0) -> tuple[float, float, float, float]:
    return (color.redF(), color.greenF(), color.blueF(), alpha)
