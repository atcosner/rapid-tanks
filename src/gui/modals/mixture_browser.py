from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter

from src.gui.widgets.mixture.mixture_info_frame import MixtureInfoFrame
from src.gui.widgets.mixture.mixture_selection_frame import MixtureSelectionFrame
from src.gui.widgets.util.dialog import Dialog


class MixtureBrowser(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Mixture Browser')

        self.splitter = QSplitter(self)
        self.selection_frame = MixtureSelectionFrame(self)
        self.info_frame = MixtureInfoFrame(self)

        self.info_frame.mixtureNameChanged.connect(self.selection_frame.handle_update_mixture_name)
        self.selection_frame.mixtureSelected.connect(self.info_frame.handle_mixture_selected)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.splitter.addWidget(self.selection_frame)
        self.splitter.addWidget(self.info_frame)

        layout = QHBoxLayout()
        layout.addWidget(self.splitter)
        self.setLayout(layout)
