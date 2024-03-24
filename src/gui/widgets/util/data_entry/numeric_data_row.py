from decimal import Decimal, InvalidOperation
from pint import Quantity

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox

from src.util.units import to_human_readable, sanitize_unit

from . import DEFAULT_MARGINS
from .util import DataEntryLineEdit


class NumericDataRow(QWidget):
    valueChanged = pyqtSignal(str)

    def __init__(
            self,
            label_string: str,
            unit: str,
            read_only: bool,
            allow_negative: bool = False,
            default: str | None = '0.0',
            precision: int = 3,
    ) -> None:
        super().__init__(None)
        self.unit = unit
        self.precision = precision

        self.previous_value: str | None = None

        self.label = QLabel(
            f'{label_string} ({to_human_readable(self.unit)})'
            if unit != 'dimensionless' else
            label_string
        )
        self.data_box = DataEntryLineEdit(allow_negative, precision)

        self.data_box.editingFinished.connect(self.handle_editing_finished)

        self._set_up_layout()
        self.set_read_only(read_only)

        if default is not None:
            self.set(default)

    def _set_up_layout(self) -> None:
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.label)
        main_layout.addStretch()
        main_layout.addWidget(self.data_box)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.data_box.setReadOnly(read_only)

    def set(self, value: str | Quantity) -> None:
        # Convert quantities to our units before we string-ify
        if isinstance(value, Quantity):
            value = value.to(sanitize_unit(self.unit))
            value = str(value.magnitude)

        self.previous_value = value
        self.data_box.setText(value)

    def get(self) -> str:
        return self.data_box.text()

    def get_decimal(self) -> Decimal | None:
        try:
            return Decimal(self.data_box.text())
        except InvalidOperation:
            return None

    @pyqtSlot()
    def handle_editing_finished(self) -> None:
        current_value = self.data_box.text()
        if self.previous_value != current_value:
            self.valueChanged.emit(current_value)

        self.previous_value = current_value
