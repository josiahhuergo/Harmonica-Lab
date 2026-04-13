from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


from piano_roll.constants import piano_bar_width, time_bar_height, scroll_bar_thickness
from piano_roll.view.viewport import PianoRollViewport


button_style = """
    QPushButton {
        background-color: #313131;
        color: #8c8c8c;
        border: none;
        padding: 0;
        margin: 0;
    }
    QPushButton:hover {
        background-color: #3a3a3a;
    }
    QPushButton:pressed {
        background-color: #212121;
    }
"""


class ZoomXButtons(QWidget):
    def __init__(self, viewport: PianoRollViewport):
        super().__init__()

        self.setFixedSize(piano_bar_width, scroll_bar_thickness)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        zoom_out_button = QPushButton()
        self.zoom_out_button = zoom_out_button
        zoom_out_button.setText("-")
        zoom_in_button = QPushButton()
        self.zoom_in_button = zoom_in_button
        zoom_in_button.setText("+")
        zoom_out_button.setFixedSize(piano_bar_width // 4, scroll_bar_thickness)
        zoom_in_button.setFixedSize(piano_bar_width // 4, scroll_bar_thickness)
        zoom_out_button.setStyleSheet(button_style)
        zoom_in_button.setStyleSheet(button_style)

        zoom_in_button.pressed.connect(viewport.zoom_in_x)
        zoom_out_button.pressed.connect(viewport.zoom_out_x)

        hbox.addWidget(zoom_out_button)
        hbox.addWidget(zoom_in_button)
        hbox.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setLayout(hbox)


class ZoomYButtons(QWidget):
    def __init__(self, viewport: PianoRollViewport):
        super().__init__()

        self.setFixedSize(scroll_bar_thickness, time_bar_height)

        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        zoom_out_button = QPushButton()
        zoom_out_button.setText("-")
        zoom_in_button = QPushButton()
        zoom_in_button.setText("+")
        zoom_out_button.setFixedSize(scroll_bar_thickness, time_bar_height // 2)
        zoom_in_button.setFixedSize(scroll_bar_thickness, time_bar_height // 2)
        zoom_out_button.setStyleSheet(button_style)
        zoom_in_button.setStyleSheet(button_style)

        zoom_in_button.pressed.connect(viewport.zoom_in_y)
        zoom_out_button.pressed.connect(viewport.zoom_out_y)

        vbox.addWidget(zoom_out_button)
        vbox.addWidget(zoom_in_button)
        self.setLayout(vbox)
