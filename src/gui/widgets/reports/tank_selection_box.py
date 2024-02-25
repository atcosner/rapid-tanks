from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton

from src.database.definitions.facility import Facility
from src.gui.widgets.tank.tank_tree import TankTree
from src.gui.widgets.util.search_bar import SearchBar


class TankSelectionBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__('Tank Selection', parent)

        self.search_bar = SearchBar(self)
        self.all_available_tanks = TankTree(self)
        self.selected_tanks = TankTree(self)

        self.add_button = QPushButton('Add')
        self.remove_button = QPushButton('Remove')

        # Signals
        self.search_bar.textChanged.connect(self.all_available_tanks.handle_search)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.all_available_tanks.setMaximumHeight(300)
        self.selected_tanks.setMaximumHeight(300)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(self.all_available_tanks)

        middle_layout = QVBoxLayout()
        middle_layout.addStretch()
        middle_layout.addWidget(self.add_button)
        middle_layout.addWidget(self.remove_button)
        middle_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.selected_tanks)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addLayout(left_layout)
        layout.addLayout(middle_layout)
        layout.addLayout(right_layout)

    def load(self, facility: Facility) -> None:
        self.all_available_tanks.load(facility)
