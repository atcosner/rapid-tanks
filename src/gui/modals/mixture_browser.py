from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout

from src.gui.widgets.mixture.mixture_info_frame import MixtureInfoFrame
from src.gui.widgets.mixture.mixture_selection_frame import MixtureSelectionFrame
from src.gui.widgets.util.dialog import Dialog


class MixtureBrowser(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Mixture Browser')

        self.create_mixture = QPushButton('Create Mixture', self)
        self.selection_frame = MixtureSelectionFrame(self)
        self.info_frame = MixtureInfoFrame(self)

        self.selection_frame.mixtureSelected.connect(self.info_frame.handle_mixture_selected)

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

        select_layout = QVBoxLayout()
        layout.addLayout(select_layout)

        select_layout.addWidget(self.create_mixture)
        select_layout.addWidget(self.selection_frame)

        layout.addWidget(self.info_frame)
