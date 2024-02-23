from decimal import Decimal

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QLabel

from src.gui.widgets.util.constants import MONTH_NAMES
from src.gui.widgets.util.data_entry.monthly_usage_data_row import MonthlyUsageDataRow
from src.gui.widgets.util.editable_frame import EditableFrame
from src.gui.widgets.util.labels import SubSectionHeader
from src.gui.widgets.util.models.mixture_model import MixtureModel


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
        self.month_lines: list[MonthlyUsageDataRow] = []
        for month in MONTH_NAMES:
            month_row = self.register_control(MonthlyUsageDataRow(month, start_read_only, self.mixture_model))
            month_row.throughputUpdated.connect(self.handle_throughput_updated)
            self.month_lines.append(month_row)

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
        for idx, month in enumerate(self.month_lines):
            months_layout.addWidget(month.checkbox, idx + 1, 0)
            months_layout.addWidget(month.throughput, idx + 1, 2)
            months_layout.addWidget(month.mixture, idx + 1, 3)
        months_layout.addLayout(total_layout, len(months_layout) + 2, 2)

        main_layout.addLayout(months_layout)
        main_layout.addLayout(self.edit_button_layout)

    def unload(self) -> None:
        self.current_tank_id = None

        for month in self.month_lines:
            month.clear()

        super().handle_end_editing()

    @pyqtSlot()
    def handle_throughput_updated(self) -> None:
        total = Decimal('0.0')

        for month in self.month_lines:
            if (month_throughput := month.get_throughput()) is not None:
                total += month_throughput

        self.throughput_total.setText(str(total))

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        # Handle saving the new data or returning to the old data
        if save:
            pass
        else:
            pass

        super().handle_end_editing()
