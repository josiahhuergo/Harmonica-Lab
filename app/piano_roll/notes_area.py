from PySide6.QtWidgets import QHBoxLayout, QScrollArea, QSizePolicy, QWidget
from PySide6.QtGui import QPainter, QColor


class NotesAreaContent(QWidget):
    """Area that can be scrolled around."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(2000, 2000)


class NotesArea(QWidget):
    def __init__(self):
        super().__init__()

        self._setup_scroll()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        print(self.size())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("pink"))

    def _setup_scroll(self):
        layout = QHBoxLayout()
        scroll_area = QScrollArea()
        scroll_area.setContentsMargins(0, 0, 0, 0)
        content = NotesAreaContent()
        scroll_area.setWidget(content)
        layout.addWidget(scroll_area)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
