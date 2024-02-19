from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from src.gui.widgets.material.material_selection_frame import MaterialSelectionFrame
from src.gui.widgets.util.dialog import Dialog


class MaterialBrowser(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Material Browser')

        self.selection_frame = MaterialSelectionFrame(self)
        self.close_button = QPushButton('Close')

        self.close_button.pressed.connect(self.reject)

        self._initial_setup()

    def _initial_setup(self) -> None:
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        layout = QVBoxLayout()
        layout.addWidget(self.selection_frame)
        layout.addLayout(button_layout)
        self.setLayout(layout)
