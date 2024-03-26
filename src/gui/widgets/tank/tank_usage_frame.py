from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QLabel

from src.database import DB_ENGINE
from src.database.definitions.fixed_roof_tank import FixedRoofTank
from src.database.definitions.service_record import ServiceRecord
from src.gui.widgets.util.constants import MONTH_NAMES
from src.gui.widgets.util.data_entry.monthly_usage_data_row import MonthlyUsageDataRow
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.labels import SubSectionHeader
from src.gui.widgets.util.message_boxes import confirm_dirty_cancel, warn_mandatory_fields
from src.gui.widgets.util.models.mixture_model import MixtureModel


@dataclass
class ServiceRecordShim:
    start_date: date
    throughput: str
    mixture_id: int


@dataclass
class TankShim:
    id: int
    service_records: list[ServiceRecordShim] = field(default_factory=list)


class TankUsageFrame(EditableFrame):
    def __init__(
            self,
            parent: QWidget,
            start_read_only: bool,
    ) -> None:
        super().__init__(parent)

        self.current_tank_id: int | None = None
        self.mixture_model = MixtureModel()

        self.throughput_total = QLabel('0.0')
        self.month_lines: dict[int, MonthlyUsageDataRow] = {}  # Month index starts @ 1
        for idx, month in enumerate(MONTH_NAMES):
            month_row = self.register_control(MonthlyUsageDataRow(month, start_read_only, self.mixture_model))
            month_row.throughputUpdated.connect(self.handle_throughput_updated)
            self.month_lines[idx + 1] = month_row

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
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        total_layout = QHBoxLayout()
        total_layout.addWidget(SubSectionHeader('Total (gal/yr): '))
        total_layout.addWidget(self.throughput_total)
        total_layout.addStretch()

        # The month data rows have layouts, but we manually use a grid since we have lots of elements to align
        months_layout = QGridLayout()
        months_layout.setColumnStretch(1, 1)
        months_layout.addWidget(SubSectionHeader('Throughput (gal/yr)'), 0, 2)
        months_layout.addWidget(SubSectionHeader('Mixture'), 0, 3)
        for month_idx, month in self.month_lines.items():
            months_layout.addWidget(month.checkbox, month_idx, 0)
            months_layout.addWidget(month.throughput, month_idx, 2)
            months_layout.addWidget(month.mixture, month_idx, 3)
        months_layout.addLayout(total_layout, len(months_layout) + 2, 2)

        main_layout.addLayout(months_layout)
        main_layout.addLayout(self.edit_button_layout)

    def load(self, tank: FixedRoofTank | TankShim) -> None:
        self.current_tank_id = tank.id
        for record in tank.service_records:
            # TODO: Handle dates correctly
            if record.start_date.day == 1:
                # Assume that a start date on the first day of the month is for the whole month
                month = self.month_lines[record.start_date.month]
                month.load(enabled=True, throughput=record.throughput, mixture_id=record.mixture_id)

    def unload(self) -> None:
        self.current_tank_id = None
        for month in self.month_lines.values():
            month.clear()

        super().handle_end_editing()

    def check(self) -> bool:
        # TODO: Check that at least one month is enabled?
        return True

    def get_current_values(self) -> TankShim:
        tank = TankShim(id=self.current_tank_id)
        for idx, month_row in self.month_lines.items():
            if month_row.is_enabled():
                tank.service_records.append(
                    ServiceRecordShim(
                        start_date=date(2000, month=idx, day=1),
                        throughput=str(month_row.get_throughput()),
                        mixture_id=month_row.get_mixture_id(),
                    )
                )

        return tank

    def update_service_records(self) -> None:
        with Session(DB_ENGINE) as session:
            tank = session.get(FixedRoofTank, self.current_tank_id)

            service_records = []
            for idx, month_row in self.month_lines.items():
                if month_row.is_enabled():
                    record = ServiceRecord(
                        start_date=date(2024, month=idx, day=1),
                        end_date=date(2024, month=idx, day=1),
                        # TODO: Add the Decimal to sqlalchemy type map
                        throughput=str(month_row.get_throughput()),
                    )
                    record.mixture_id = month_row.get_mixture_id()
                    service_records.append(record)

            tank.service_records = service_records
            session.commit()

    @pyqtSlot()
    def handle_throughput_updated(self) -> None:
        total = Decimal('0.0')

        for month in self.month_lines.values():
            if month.is_enabled():
                if (month_throughput := month.get_throughput()) is not None:
                    total += month_throughput

        self.throughput_total.setText(str(total))

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        self.previous_values = self.get_current_values()
        super().handle_begin_editing()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle saving the new data or returning to the old data
        if save:
            if self.check():
                # Only emit updates that actually change state
                if self.previous_values != self.get_current_values():
                    self.update_service_records()
            else:
                return warn_mandatory_fields(self)
        else:
            # Prompt the user to confirm they are deleting unsaved data
            if self.is_dirty() and not confirm_dirty_cancel(self):
                return

            self.load(self.previous_values)

        super().handle_end_editing()
