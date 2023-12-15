from PyQt5.Qt import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QFrame, QGridLayout, QPushButton, QVBoxLayout,
)

from src.components.fixed_roof_tank import VerticalFixedRoofTank

from src.gui import RESOURCE_DIR
from src.gui.widgets.util.data_entry_rows import (
    NumericDataRow, CheckBoxDataRow, ComboBoxDataRow, ComboBoxDataType,
)
from src.gui.widgets.util.labels import SubSectionHeader
from src.util.errors import DataEntryResult


class VerticalPhysicalFrame(QFrame):
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
        dimensions_layout.addWidget(self.shell_height)
        dimensions_layout.addWidget(self.shell_diameter)
        dimensions_layout.addWidget(self.max_liquid_height)
        dimensions_layout.addWidget(self.avg_liquid_height)
        dimensions_layout.addWidget(self.working_volume)
        dimensions_layout.addWidget(self.turnovers_per_year)
        dimensions_layout.addWidget(self.net_throughput)
        dimensions_layout.addWidget(self.is_heated)
        dimensions_layout.addStretch()
        self.setLayout(dimensions_layout)

        # Shell Characteristics
        shell_layout = QVBoxLayout()
        main_layout.addLayout(shell_layout, 1, 0)

        shell_layout.addStretch()
        shell_layout.addWidget(SubSectionHeader('Shell Characteristics'))
        shell_layout.addWidget(self.shell_color)
        shell_layout.addWidget(self.shell_condition)

        # Roof Characteristics
        roof_layout = QVBoxLayout()
        main_layout.addLayout(roof_layout, 0, 1)

        roof_layout.addWidget(SubSectionHeader('Roof Characteristics'))
        roof_layout.addWidget(self.roof_color)
        roof_layout.addWidget(self.roof_condition)
        roof_layout.addWidget(self.roof_type)
        roof_layout.addWidget(self.roof_height)
        roof_layout.addWidget(self.roof_radius)
        roof_layout.addWidget(self.roof_slope)
        roof_layout.addStretch()

        # Breather Vent Settings
        vent_layout = QVBoxLayout()
        main_layout.addLayout(vent_layout, 1, 1)

        vent_layout.addStretch()
        vent_layout.addWidget(SubSectionHeader('Breather Vent Settings'))
        vent_layout.addWidget(self.vacuum_setting)
        vent_layout.addWidget(self.pressure_setting)

        # Set up the dynamic nature of the roof type
        self.roof_type.selectionChanged.connect(self.handle_roof_type_change)
        self.handle_roof_type_change(self.roof_type.get_selected())

        if self.read_only:
            main_layout.addWidget(self.edit_button, 0, 2)

    @pyqtSlot(str)
    def handle_roof_type_change(self, new_type: str) -> None:
        if new_type == 'Dome':
            self.roof_slope.hide()
            self.roof_radius.show()
        elif new_type == 'Cone':
            self.roof_slope.show()
            self.roof_radius.hide()
        else:
            raise RuntimeError(f'Unexpected roof type: "{new_type}"')

    def load(self, tank: VerticalFixedRoofTank) -> None:
        # Check that we got the right type
        if not isinstance(tank, VerticalFixedRoofTank):
            raise RuntimeError(f'Incompatible tank type: {type(tank)}')

        self.shell_height.set(tank.height)
        self.shell_diameter.set(tank.diameter)
        # self.max_liquid_height = NumericDataRow('Maximum Liquid Height', 'ft', read_only)
        # self.avg_liquid_height = NumericDataRow('Average Liquid Height', 'ft', read_only)
        # self.working_volume = NumericDataRow('Working Volume', 'gal', read_only)
        # self.turnovers_per_year = NumericDataRow('Turnovers Per Year', 'dimensionless', read_only)
        # self.net_throughput = NumericDataRow('Net Throughput', 'gal/yr', read_only)
        # self.is_heated = CheckBoxDataRow('Is Heated?', read_only)

        # self.shell_color = ComboBoxDataRow('Shell Color', ComboBoxDataType.PAINT_COLORS, read_only)
        # self.shell_condition = ComboBoxDataRow('Shell Condition', ComboBoxDataType.PAINT_CONDITIONS, read_only)
        #
        # self.roof_color = ComboBoxDataRow('Roof Color', ComboBoxDataType.PAINT_COLORS, read_only)
        # self.roof_condition = ComboBoxDataRow('Roof Condition', ComboBoxDataType.PAINT_CONDITIONS, read_only)
        # self.roof_type = ComboBoxDataRow('Roof Type', ['Cone', 'Dome'], read_only)
        self.roof_height.set(tank.roof_height)
        self.roof_radius.set(tank.roof_radius)
        self.roof_slope.set(tank.roof_slope)

        # self.vacuum_setting.set()
        # self.pressure_setting.set()

    def check(self) -> DataEntryResult:
        # TODO: Check for some valid data
        return DataEntryResult(True, [])

    def build(self) -> VerticalFixedRoofTank:
        # TODO: Reconcile the other parameters that we need
        return VerticalFixedRoofTank(
            identifier='',
            diameter=self.shell_diameter.get(),
            height=self.shell_height.get(),
            liquid_height=self.avg_liquid_height.get(),

            roof_height=self.roof_height.get(),
            roof_slope=self.roof_slope.get(),
            roof_radius=self.roof_radius.get(),
        )
