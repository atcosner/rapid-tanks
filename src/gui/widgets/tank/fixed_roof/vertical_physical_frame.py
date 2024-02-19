from sqlalchemy import select
from sqlalchemy.orm import Session
from types import SimpleNamespace

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from src.database import DB_ENGINE
from src.database.definitions.paint import PaintColor, PaintCondition
from src.database.definitions.tank import FixedRoofTank, FixedRoofType
from src.gui.widgets.util.data_entry.combo_box_data_row import ComboBoxDataRow, ComboBoxDataType
from src.gui.widgets.util.data_entry.numeric_data_row import NumericDataRow
from src.gui.widgets.util.data_entry_rows import CheckBoxDataRow
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.labels import SubSectionHeader
from src.gui.widgets.util.message_boxes import confirm_dirty_cancel, warn_mandatory_fields


class VerticalPhysicalFrame(EditableFrame):
    def __init__(self, parent: QWidget, start_read_only: bool) -> None:
        super().__init__(parent)
        self.current_tank_id: int | None = None

        # Dimensions
        self.shell_height = self.register_control(NumericDataRow('Shell Height', 'ft', start_read_only))
        self.shell_diameter = self.register_control(NumericDataRow('Shell Diameter', 'ft', start_read_only))
        self.max_liquid_height = self.register_control(NumericDataRow('Maximum Liquid Height', 'ft', start_read_only))
        self.avg_liquid_height = self.register_control(NumericDataRow('Average Liquid Height', 'ft', start_read_only))
        self.working_volume = self.register_control(NumericDataRow('Working Volume', 'gal', start_read_only))
        self.turnovers_per_year = self.register_control(NumericDataRow('Turnovers Per Year', 'dimensionless', start_read_only))
        self.net_throughput = self.register_control(NumericDataRow('Net Throughput', 'gal/yr', start_read_only))
        self.is_heated = self.register_control(CheckBoxDataRow('Is Heated?', start_read_only))

        # Shell Characteristics
        self.shell_color = self.register_control(ComboBoxDataRow('Shell Color', ComboBoxDataType.PAINT_COLORS, start_read_only))
        self.shell_condition = self.register_control(ComboBoxDataRow('Shell Condition', ComboBoxDataType.PAINT_CONDITIONS, start_read_only))

        # Roof Characteristics
        self.roof_color = self.register_control(ComboBoxDataRow('Roof Color', ComboBoxDataType.PAINT_COLORS, start_read_only))
        self.roof_condition = self.register_control(ComboBoxDataRow('Roof Condition', ComboBoxDataType.PAINT_CONDITIONS, start_read_only))
        self.roof_type = self.register_control(ComboBoxDataRow('Roof Type', ComboBoxDataType.ROOF_TYPES, start_read_only))
        self.roof_height = self.register_control(NumericDataRow('Roof Height', 'ft', start_read_only))
        self.roof_radius = self.register_control(NumericDataRow('Radius', 'ft', start_read_only))
        self.roof_slope = self.register_control(NumericDataRow('Slope', 'ft/ft', start_read_only, default='0.0625'))

        # Breather Vent Settings
        self.vacuum_setting = self.register_control(
            NumericDataRow(
                'Vacuum Setting',
                'psig',
                start_read_only,
                allow_negative=True,
                default='-0.3',
            )
        )
        self.pressure_setting = self.register_control(
            NumericDataRow(
                'Pressure Setting',
                'psig',
                start_read_only,
                default='0.3',
            )
        )

        # Set up the dynamic nature of the roof type
        self.roof_type.selectionChanged.connect(self.handle_roof_type_change)
        self.handle_roof_type_change(self.roof_type.get_selected_text())

        if start_read_only:
            super().handle_end_editing()
        else:
            super().handle_begin_editing()

        # Register our edit handlers
        self.register_edit_handlers(
            begin_func=self.handle_begin_editing,
            end_close_func=lambda: self.handle_end_editing(False),
            end_save_func=lambda: self.handle_end_editing(True),
        )

        self._set_up_layout()

    def _set_up_layout(self) -> None:
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

        # Edit controls
        main_layout.addLayout(self.edit_button_layout, 0, 2)

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

    def load(self, tank: FixedRoofTank) -> None:
        self.current_tank_id = tank.id

        self.shell_height.set(tank.shell_height)
        self.shell_diameter.set(tank.shell_diameter)
        self.max_liquid_height.set(tank.maximum_liquid_height)
        self.avg_liquid_height.set(tank.average_liquid_height)
        self.working_volume.set(tank.working_volume)
        self.turnovers_per_year.set(tank.turnovers_per_year)
        self.net_throughput.set(tank.net_throughput)
        self.is_heated.set(tank.is_heated)

        self.shell_color.set_from_db(tank.shell_paint_color.id)
        self.shell_condition.set_from_db(tank.shell_paint_condition.id)

        self.roof_color.set_from_db(tank.roof_paint_color.id)
        self.roof_condition.set_from_db(tank.roof_paint_condition.id)
        self.roof_type.set_from_db(tank.roof_type.id)
        self.roof_height.set(tank.roof_height)
        self.roof_radius.set(tank.roof_radius)
        self.roof_slope.set(tank.roof_slope)

        self.vacuum_setting.set(tank.vent_vacuum_setting)
        self.pressure_setting.set(tank.vent_breather_setting)

    def unload(self) -> None:
        self.current_tank_id = None

        dummy_tank = FixedRoofTank(name='')
        dummy_tank.shell_paint_color = SimpleNamespace(id=1)
        dummy_tank.shell_paint_condition = SimpleNamespace(id=1)
        dummy_tank.roof_paint_color = SimpleNamespace(id=1)
        dummy_tank.roof_paint_condition = SimpleNamespace(id=1)
        dummy_tank.roof_type = SimpleNamespace(id=1)
        self.load(dummy_tank)

        super().handle_end_editing()

    def check(self) -> bool:
        # TODO: Check for some valid data
        return True

    def update_tank(self, existing_tank: FixedRoofTank | None) -> FixedRoofTank:
        tank = existing_tank if existing_tank is not None else FixedRoofTank(name='test')

        with Session(DB_ENGINE) as session:
            tank.shell_height = self.shell_height.get()
            tank.shell_diameter = self.shell_diameter.get()
            tank.maximum_liquid_height = self.max_liquid_height.get()
            tank.average_liquid_height = self.avg_liquid_height.get()
            tank.working_volume = self.working_volume.get()
            tank.turnovers_per_year = self.turnovers_per_year.get()
            tank.net_throughput = self.net_throughput.get()
            tank.is_heated = self.is_heated.get()

            tank.shell_paint_color = session.scalar(select(PaintColor).where(PaintColor.id == self.shell_color.get_selected_db_id()))
            tank.shell_paint_condition = session.scalar(select(PaintCondition).where(PaintCondition.id == self.shell_condition.get_selected_db_id()))

            tank.roof_paint_color = session.scalar(select(PaintColor).where(PaintColor.id == self.roof_color.get_selected_db_id()))
            tank.roof_paint_condition = session.scalar(select(PaintCondition).where(PaintCondition.id == self.roof_condition.get_selected_db_id()))
            tank.roof_type = session.scalar(select(FixedRoofType).where(FixedRoofType.id == self.roof_type.get_selected_db_id()))
            tank.roof_height = self.roof_height.get()
            tank.roof_radius = self.roof_radius.get()
            tank.roof_slope = self.roof_slope.get()

            tank.vent_vacuum_setting = self.vacuum_setting.get()
            tank.vent_breather_setting = self.pressure_setting.get()

        return tank

    def write_tank_to_db(self) -> int:
        with Session(DB_ENGINE) as session:
            tank = session.get(FixedRoofTank, self.current_tank_id)
            self.update_tank(existing_tank=tank)
            session.commit()

        return self.current_tank_id

    def get_current_values(self) -> FixedRoofTank:
        return self.update_tank(existing_tank=None)

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

        # Save the current state
        self.previous_values = self.get_current_values()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle saving the new data or returning to the old data
        if save:
            if self.check():
                if self.previous_values != self.get_current_values():
                    self.write_tank_to_db()
            else:
                return warn_mandatory_fields(self)
        else:
            # Prompt the user to confirm they are deleting unsaved data
            if self.is_dirty() and not confirm_dirty_cancel(self):
                return

            self.load(self.previous_values)

        super().handle_end_editing()
