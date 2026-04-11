from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from PySide6.QtCore import QEvent, QSize, Qt

from piano_roll.colors import Colors
from piano_roll.events import piano_roll_events as events
from piano_roll.state import piano_roll_state as state
from piano_roll.views.notes_area import NotesArea
from piano_roll.views.piano_bar import PianoBar
from piano_roll.views.time_bar import TimeBar


class Corner(QWidget):
    """Empty placeholder widget."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(state.piano_bar_width, state.time_bar_height))

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setBrush(Colors.BG_BLACK)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())


class PianoRoll(QWidget):
    """A piano roll for editing and playing back note data."""

    def __init__(self):
        super().__init__()

        # Initializes the different areas of the piano roll
        self.time_bar = TimeBar()
        self.piano_bar = PianoBar()
        self.notes_area = NotesArea()
        self.corner = Corner()

        self._setup_layout()
        self._setup_sync()

        # Emits resized signal to initialize some state
        events.resized.emit(self.rect().size())

    def _setup_layout(self):
        top_hbox = QHBoxLayout()
        top_hbox.setContentsMargins(0, 0, 0, 0)
        top_hbox.setSpacing(0)
        top_hbox.addWidget(self.corner)
        top_hbox.addWidget(self.time_bar)

        bottom_hbox = QHBoxLayout()
        bottom_hbox.setContentsMargins(0, 0, 0, 0)
        bottom_hbox.setSpacing(0)
        bottom_hbox.addWidget(self.piano_bar)
        bottom_hbox.addWidget(self.notes_area)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addLayout(top_hbox)
        layout.addLayout(bottom_hbox)

        self.setLayout(layout)

    def _setup_sync(self):
        self.piano_bar.scroll_area.viewport().installEventFilter(self)
        self.time_bar.scroll_area.viewport().installEventFilter(self)
        self.notes_area.scroll_area.viewport().installEventFilter(self)

        sb_h = self.notes_area.scroll_area.horizontalScrollBar()
        sb_v = self.notes_area.scroll_area.verticalScrollBar()

        sb_h.sliderMoved.connect(lambda: events.scrolled.emit())
        sb_v.sliderMoved.connect(self.piano_bar.set_scroll_y)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Wheel:
            self.wheelEvent(event)
            return True  # stop the event from being handled by the child
        return super().eventFilter(obj, event)

    def wheelEvent(self, event):
        state.scroll((event.angleDelta().x(), event.angleDelta().y()))
        event.accept()
