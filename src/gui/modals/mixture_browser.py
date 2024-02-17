from sqlalchemy.orm import Session
from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout

from src.database import DB_ENGINE
from src.database.definitions.mixture import PetrochemicalMixture
from src.gui.widgets.mixture.mixture_info_frame import MixtureInfoFrame
from src.gui.widgets.mixture.mixture_selection_frame import MixtureSelectionFrame
from src.gui.widgets.util.dialog import Dialog


class MixtureBrowser(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Mixture Browser')

        self.create_mixture_button = QPushButton('Create Mixture', self)
        self.selection_frame = MixtureSelectionFrame(self)
        self.info_frame = MixtureInfoFrame(self)

        self.info_frame.mixtureNameChanged.connect(self.selection_frame.handle_update_mixture_name)
        self.selection_frame.mixtureSelected.connect(self.info_frame.handle_mixture_selected)
        self.create_mixture_button.clicked.connect(self.create_mixture)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.create_mixture_button.setAutoDefault(False)

        layout = QHBoxLayout()
        self.setLayout(layout)

        select_layout = QVBoxLayout()
        layout.addLayout(select_layout)

        select_layout.addWidget(self.create_mixture_button)
        select_layout.addWidget(self.selection_frame)

        layout.addWidget(self.info_frame)

    @pyqtSlot()
    def create_mixture(self) -> None:
        with Session(DB_ENGINE) as session:
            session.add(
                PetrochemicalMixture(
                    name=f'New Mixture ({session.query(PetrochemicalMixture.id).count()})',
                )
            )
            session.commit()

        self.selection_frame.reload()
