from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QGridLayout, QPushButton, QVBoxLayout,
)

from src.components.tank import Tank

from src.gui import RESOURCE_DIR
from src.gui.widgets.util.data_entry_rows import NumericDataRow, CheckboxDataRow
from src.gui.widgets.util.labels import SubSectionHeader


class TankPhysicalFrame(QFrame):
    def __init__(self, parent: QWidget, read_only: bool) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.read_only = read_only
        self.edit_button = QPushButton()

        # Dimensions
        self.shell_height = NumericDataRow('Shell Height', 'ft', read_only)
        self.shell_diameter = NumericDataRow('Shell Diameter', 'ft', read_only)
        self.max_liquid_height = NumericDataRow('Maximum Liquid Height', 'ft', read_only)
        self.avg_liquid_height = NumericDataRow('Average Liquid Height', 'ft', read_only)
        self.working_volume = NumericDataRow('Working Volume', 'gal', read_only)
        self.turnovers_per_year = NumericDataRow('Turnovers Per Year', 'dimensionless', read_only)
        self.net_throughput = NumericDataRow('Net Throughput', 'gal/yr', read_only)
        self.is_heated = CheckboxDataRow('Is Heated?', read_only)

        self._initial_setup()

    def _initial_setup(self) -> None:
        # Set up the edit button
        # TODO: Open a tank edit window
        self.edit_button.setIcon(QIcon(str(RESOURCE_DIR / 'pencil.png')))
        self.edit_button.setMaximumSize(65, 65)

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Dimensions
        dimensions_layout = QVBoxLayout()
        main_layout.addLayout(dimensions_layout, 0, 0)

        dimensions_layout.addWidget(SubSectionHeader('Dimensions'))
        dimensions_layout.addLayout(self.shell_height)
        dimensions_layout.addLayout(self.shell_diameter)
        dimensions_layout.addLayout(self.max_liquid_height)
        dimensions_layout.addLayout(self.avg_liquid_height)
        dimensions_layout.addLayout(self.working_volume)
        dimensions_layout.addLayout(self.turnovers_per_year)
        dimensions_layout.addLayout(self.net_throughput)
        dimensions_layout.addLayout(self.is_heated)

        if self.read_only:
            main_layout.addWidget(self.edit_button, 0, 2)

    def load(self, tank: Tank) -> None:
        pass
