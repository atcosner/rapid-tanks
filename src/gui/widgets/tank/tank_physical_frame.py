from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QLineEdit, QGridLayout, QPushButton, QCheckBox,
)

from src.components.tank import Tank

from src.gui import RESOURCE_DIR


class TankPhysicalFrame(QFrame):
    def __init__(self, parent: QWidget, read_only: bool) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.read_only = read_only
        self.edit_button = QPushButton()

        # Dimensions
        self.shell_height = QLineEdit()
        self.shell_diameter = QLineEdit()
        self.max_liquid_height = QLineEdit()
        self.avg_liquid_height = QLineEdit()
        self.working_volume = QLineEdit()
        self.turnovers_per_year = QLineEdit()
        self.net_throughput = QLineEdit()
        self.is_heated = QCheckBox()

        self._initial_setup()

    def _initial_setup(self) -> None:
        # All the widgets should match our read-only status
        self.shell_height.setReadOnly(self.read_only)
        self.shell_diameter.setReadOnly(self.read_only)
        self.max_liquid_height.setReadOnly(self.read_only)
        self.avg_liquid_height.setReadOnly(self.read_only)
        self.working_volume.setReadOnly(self.read_only)
        self.turnovers_per_year.setReadOnly(self.read_only)
        self.net_throughput.setReadOnly(self.read_only)
        self.is_heated.setDisabled(self.read_only)

        # Set up the edit button
        # TODO: Open a tank edit window
        self.edit_button.setIcon(QIcon(str(RESOURCE_DIR / 'pencil.png')))
        self.edit_button.setMaximumSize(65, 65)

        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Dimensions
        dimensions_layout = QGridLayout()
        main_layout.addLayout(dimensions_layout, 0, 0)
        dimensions_layout.addWidget(QLabel('Dimensions'), 0, 0)

        dimensions_layout.addWidget(QLabel('Shell Height'), 1, 0)
        dimensions_layout.addWidget(self.shell_height, 1, 1)
        dimensions_layout.addWidget(QLabel('Shell Diameter'), 2, 0)
        dimensions_layout.addWidget(self.shell_diameter, 2, 1)
        dimensions_layout.addWidget(QLabel('Max Liquid Height'), 3, 0)
        dimensions_layout.addWidget(self.max_liquid_height, 3, 1)
        dimensions_layout.addWidget(QLabel('Average Liquid Height'), 4, 0)
        dimensions_layout.addWidget(self.avg_liquid_height, 4, 1)
        dimensions_layout.addWidget(QLabel('Working Volume'), 5, 0)
        dimensions_layout.addWidget(self.working_volume, 5, 1)
        dimensions_layout.addWidget(QLabel('Turnovers Per Year'), 6, 0)
        dimensions_layout.addWidget(self.turnovers_per_year, 6, 1)
        dimensions_layout.addWidget(QLabel('Net Throughput'), 7, 0)
        dimensions_layout.addWidget(self.net_throughput, 7, 1)
        dimensions_layout.addWidget(QLabel('Heated?'), 8, 0)
        dimensions_layout.addWidget(self.is_heated, 8, 1)

        if self.read_only:
            main_layout.addWidget(self.edit_button, 0, 2)

    def load(self, tank: Tank) -> None:
        pass
