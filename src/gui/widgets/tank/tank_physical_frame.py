from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QGridLayout, QPushButton, QVBoxLayout,
)

from src.components.tank import Tank

from src.gui import RESOURCE_DIR
from src.gui.widgets.util.data_entry_rows import (
    NumericDataRow, CheckBoxDataRow, ComboBoxDataRow, ComboBoxDataType,
)
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
        self.is_heated = CheckBoxDataRow('Is Heated?', read_only)

        # Shell Characteristics
        self.shell_color = ComboBoxDataRow('Shell Color', ComboBoxDataType.PAINT_COLORS, read_only)
        self.shell_condition = ComboBoxDataRow('Shell Condition', ComboBoxDataType.PAINT_CONDITIONS, read_only)

        # Roof Characteristics
        self.roof_color = ComboBoxDataRow('Roof Color', ComboBoxDataType.PAINT_COLORS, read_only)
        self.roof_condition = ComboBoxDataRow('Roof Condition', ComboBoxDataType.PAINT_CONDITIONS, read_only)
        self.roof_type = ComboBoxDataRow('Roof Type', ['Cone', 'Dome'], read_only)
        self.roof_height = NumericDataRow('Roof Height', 'ft', read_only)
        self.roof_radius = NumericDataRow('Radius', 'ft', read_only)
        self.roof_slope = NumericDataRow('Slope', 'ft/ft', read_only, default='0.0625')

        # Breather Vent Settings
        self.vacuum_setting = NumericDataRow(
            'Vacuum Setting', 'psig', read_only, allow_negative=True, default='-0.3',
        )
        self.pressure_setting = NumericDataRow(
            'Pressure Setting', 'psig', read_only, default='0.3',
        )

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
        dimensions_layout.addStretch()

        # Shell Characteristics
        shell_layout = QVBoxLayout()
        main_layout.addLayout(shell_layout, 1, 0)

        shell_layout.addStretch()
        shell_layout.addWidget(SubSectionHeader('Shell Characteristics'))
        shell_layout.addLayout(self.shell_color)
        shell_layout.addLayout(self.shell_condition)

        # Roof Characteristics
        roof_layout = QVBoxLayout()
        main_layout.addLayout(roof_layout, 0, 1)

        roof_layout.addWidget(SubSectionHeader('Roof Characteristics'))
        roof_layout.addLayout(self.roof_color)
        roof_layout.addLayout(self.roof_condition)
        roof_layout.addLayout(self.roof_type)
        roof_layout.addLayout(self.roof_height)
        roof_layout.addLayout(self.roof_radius)
        roof_layout.addLayout(self.roof_slope)
        roof_layout.addStretch()

        # Breather Vent Settings
        vent_layout = QVBoxLayout()
        main_layout.addLayout(vent_layout, 1, 1)

        vent_layout.addStretch()
        vent_layout.addWidget(SubSectionHeader('Breather Vent Settings'))
        vent_layout.addLayout(self.vacuum_setting)
        vent_layout.addLayout(self.pressure_setting)

        if self.read_only:
            main_layout.addWidget(self.edit_button, 0, 2)

    def load(self, tank: Tank) -> None:
        pass
