from PyQt5.QtWidgets import QWidget, QGroupBox, QHBoxLayout, QVBoxLayout, QPushButton, QLabel

from src.components.tank import TankType
from src.database.definitions.facility import Facility
from src.gui.widgets.tank.tank_tree import TankTree
from src.gui.widgets.util.search_bar import SearchBar


class TankSelectionBox(QGroupBox):
    def __init__(self, parent: QWidget) -> None:
        super().__init__('Tank Selection', parent)

        self.search_bar = SearchBar(self)
        self.all_available_tanks = TankTree(self)
        self.selected_tanks = TankTree(self, auto_hide_children=True)

        self.add_button = QPushButton('Add')
        self.add_all_button = QPushButton('Add All')
        self.remove_button = QPushButton('Remove')

        # Signals
        self.search_bar.textChanged.connect(self.all_available_tanks.handle_search)
        self.add_button.clicked.connect(self.handle_add_tank)
        self.add_all_button.clicked.connect(self.handle_add_all_tanks)
        self.remove_button.clicked.connect(self.handle_remove_tank)

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
        middle_layout.addWidget(QLabel())  # TODO: There is probably a better way to get a spacer
        middle_layout.addWidget(self.add_all_button)
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
        self.selected_tanks.load(facility)

    def handle_add_tank(self) -> None:
        # Add the selected left side tank to the right side
        selected_tank = self.all_available_tanks.get_selected()
        if selected_tank is not None:
            self.selected_tanks.show_tank(*selected_tank)

    def handle_add_all_tanks(self) -> None:
        # TODO: Should this include hidden?
        for tank in self.all_available_tanks.get_all_tanks(include_hidden=False):
            self.selected_tanks.show_tank(*tank)

    def handle_remove_tank(self) -> None:
        self.selected_tanks.hide_selected_tank()

    def get_selected_tanks(self) -> list[tuple[TankType, int]]:
        return self.selected_tanks.get_all_tanks(include_hidden=False)
