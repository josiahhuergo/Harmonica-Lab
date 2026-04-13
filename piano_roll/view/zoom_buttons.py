from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ZoomXButtons(QWidget):
    def __init__(self):
        super().__init__()
        hbox = QHBoxLayout()
        zoom_out_button = QPushButton()
        zoom_out_button.setText("-")
        zoom_out_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        zoom_in_button = QPushButton()
        zoom_in_button.setText("+")
        zoom_in_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        hbox.addWidget(zoom_out_button)
        hbox.addWidget(zoom_in_button)
        self.setLayout(hbox)


class ZoomYButtons(QWidget):
    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        zoom_out_button = QPushButton()
        zoom_out_button.setText("-")
        zoom_out_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        zoom_in_button = QPushButton()
        zoom_in_button.setText("+")
        zoom_in_button.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        vbox.addWidget(zoom_out_button)
        vbox.addWidget(zoom_in_button)
        self.setLayout(vbox)
