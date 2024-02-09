from sqlalchemy import select
from sqlalchemy.orm import Session

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QTabWidget, QHBoxLayout

from src.database import DB_ENGINE
from src.gui.widgets.material.petrochemical_info_frame import PetrochemicalInfoFrame
from src.gui.widgets.material.petrochemical_list import PetrochemicalList
from src.gui.widgets.util.search_bar import SearchBar


class MaterialSelectionFrame(QFrame):
    siteSelected = pyqtSignal(int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.material_tabs = QTabWidget(self)
        self.petrochemical_list = PetrochemicalList(self)
        self.petrochemical_info = PetrochemicalInfoFrame(self)

        self.petrochemical_list.materialSelected.connect(self.petrochemical_info.handle_material_selected)

        self.search_bar = SearchBar(self)
        self.search_bar.textChanged.connect(self.petrochemical_list.handle_search)

        # Set up the tab widget for each type of material
        self.material_tabs.addTab(self.petrochemical_list, 'Petrochemical')

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Set up the list of materials
        list_layout = QVBoxLayout()
        list_layout.addWidget(self.search_bar)
        list_layout.addWidget(self.material_tabs)
        layout.addLayout(list_layout)

        # TODO: Petroleum liquids?
        layout.addWidget(self.petrochemical_info)
