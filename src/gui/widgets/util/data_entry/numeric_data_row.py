from pint import Quantity

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QCheckBox

from src.gui.widgets.util.validators import PositiveDoubleValidator, DoubleValidator
from src.util.units import to_human_readable, sanitize_unit

from . import DEFAULT_MARGINS


class DataEntryLineEdit(QLineEdit):
    def __init__(
            self,
            read_only: bool,
            allow_negative: bool,
            precision: int,
    ) -> None:
        super().__init__()

        # Set some defaults
        self.setReadOnly(read_only)
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setMaximumWidth(75)

        # Set up the validator
        if allow_negative:
            self.setValidator(DoubleValidator(precision))
        else:
            self.setValidator(PositiveDoubleValidator(precision))


class NumericDataRow(QWidget):
    valueChanged = pyqtSignal(str)

    def __init__(
            self,
            label_string: str,
            unit: str,
            read_only: bool,
            allow_negative: bool = False,
            default: str | None = '0.0',
            precision: int = 6,
            allow_autofill: bool = False,
    ) -> None:
        super().__init__(None)
        self.unit = unit
        self.precision = precision
        self.allow_autofill = allow_autofill

        self.previous_value: str | None = None

        self.label = QLabel(
            f'{label_string} ({to_human_readable(self.unit)})'
            if unit != 'dimensionless' else
            label_string
        )
        self.data_box = DataEntryLineEdit(read_only, allow_negative, precision)
        self.autofill_checkbox = QCheckBox('Autofill')

        self.data_box.editingFinished.connect(self.handle_editing_finished)
        self.autofill_checkbox.stateChanged.connect(self.handle_autofill_change)

        self._set_up_layout()

        if default is not None:
            self.set(default)

    def _set_up_layout(self) -> None:
        # Set up our layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addStretch()

        if self.allow_autofill:
            self.autofill_checkbox.setChecked(True)
            main_layout.addWidget(self.autofill_checkbox)

        main_layout.addWidget(self.data_box)
        self.setLayout(main_layout)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.autofill_checkbox.setDisabled(read_only)
        self.data_box.setReadOnly(read_only)

        if self.allow_autofill and self.autofill_checkbox.isChecked():
            self.data_box.setDisabled(True)
        else:
            self.data_box.setDisabled(False)

    def set(self, value: str | Quantity) -> None:
        # Convert quantities to our units before we string-ify
        if isinstance(value, Quantity):
            value = value.to(sanitize_unit(self.unit))
            value = str(value.magnitude)

        self.previous_value = value
        self.data_box.setText(value)

    def get(self) -> str:
        return self.data_box.text()

    @pyqtSlot()
    def handle_editing_finished(self) -> None:
        current_value = self.data_box.text()
        if self.previous_value != current_value:
            self.valueChanged.emit(current_value)

        self.previous_value = current_value

    @pyqtSlot()
    def handle_autofill_change(self) -> None:
        self.data_box.setDisabled(self.autofill_checkbox.isChecked())
