from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QPushButton, QHBoxLayout

from src.components.mixture import MixtureMakeup
from src.database import DB_ENGINE
from src.database.definitions.mixture import PetrochemicalMixture
from src.gui.widgets.mixture.mixture_list import MixtureList
from src.gui.widgets.util.search_bar import SearchBar


class MixtureSelectionFrame(QFrame):
    mixtureSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.create_mixture_button = QPushButton('Create Mixture')
        self.delete_mixture_button = QPushButton('Delete Mixture')
        self.search_bar = SearchBar(self)
        self.mixture_list = MixtureList(self)

        self.mixture_list.mixtureSelected.connect(self.mixtureSelected)
        self.search_bar.textChanged.connect(self.mixture_list.handle_search)
        self.create_mixture_button.clicked.connect(self.create_mixture)
        self.delete_mixture_button.clicked.connect(self.delete_selected_mixture)

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.create_mixture_button)
        buttons_layout.addWidget(self.delete_mixture_button)

        layout.addLayout(buttons_layout)
        layout.addWidget(self.search_bar)
        layout.addWidget(self.mixture_list)

    def reload(self) -> None:
        self.mixture_list.populate()

    @pyqtSlot(int, str)
    def handle_update_mixture_name(self, mixture_id: int, mixture_name: str) -> None:
        self.mixture_list.update_mixture_name(mixture_id, mixture_name)

    @pyqtSlot()
    def create_mixture(self) -> None:
        with Session(DB_ENGINE) as session:
            session.add(
                PetrochemicalMixture(
                    name=f'New Mixture ({session.query(PetrochemicalMixture.id).count()})',
                    makeup_type_id=MixtureMakeup.WEIGHT.value,
                )
            )
            session.commit()

        self.reload()

    @pyqtSlot()
    def delete_selected_mixture(self) -> None:
        self.mixture_list.delete_selected_mixture()
