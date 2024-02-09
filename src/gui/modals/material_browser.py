from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.gui.widgets.material.material_selection_frame import MaterialSelectionFrame
from src.gui.widgets.util.dialog import Dialog


class MaterialBrowser(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Material Browser')

        self.selection_frame = MaterialSelectionFrame(self)

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self.selection_frame)

        self.setLayout(layout)
