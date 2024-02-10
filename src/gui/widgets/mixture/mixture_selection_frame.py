from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout

from src.gui.widgets.mixture.mixture_list import MixtureList
from src.gui.widgets.util.search_bar import SearchBar


class MixtureSelectionFrame(QFrame):
    mixtureSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.mixture_list = MixtureList(self)

        self.mixture_list.mixtureSelected.connect(self.mixtureSelected)

        self.search_bar = SearchBar(self)
        self.search_bar.textChanged.connect(self.mixture_list.handle_search)

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.search_bar)
        layout.addWidget(self.mixture_list)
