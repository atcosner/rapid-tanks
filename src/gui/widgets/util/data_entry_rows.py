from collections.abc import Iterable
from decimal import Decimal
from enum import Enum, auto
from pint import Quantity

from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox

from src.util.units import to_human_readable

from .validators import NonZeroDoubleValidator, DoubleValidator


class ComboBoxDataType(Enum):
    PAINT_COLORS = auto()
    PAINT_CONDITIONS = auto()


class DataEntryLineEdit(QLineEdit):
    def __init__(self, read_only: bool, allow_negative: bool) -> None:
        super().__init__()

        # Set some defaults
        self.setReadOnly(read_only)
        self.setMaximumWidth(100)
        self.setAlignment(QtCore.Qt.AlignRight)

        # Set up the validator
        if allow_negative:
            self.setValidator(DoubleValidator())
        else:
            self.setValidator(NonZeroDoubleValidator())


class NumericDataRow(QHBoxLayout):
    def __init__(
            self,
            label_string: str,
            unit: str,
            read_only: bool,
            allow_negative: bool = False,
            default: str | None = None,
    ) -> None:
        super().__init__(None)
        self.unit = unit

        self.label = QLabel(
            f'{label_string} ({to_human_readable(unit)})'
            if unit != 'dimensionless' else
            label_string
        )
        self.data_box = DataEntryLineEdit(read_only, allow_negative)

        self.addWidget(self.label)
        self.addStretch()
        self.addWidget(self.data_box)

        if default is not None:
            self.data_box.setPlaceholderText(default)

    def set_text(self, value: Quantity | str) -> None:
        if isinstance(value, str):
            self.data_box.setText(value)
        else:
            # Convert to our unit
            converted_value = value.to(self.unit)

            # Limit to 6 decimal places
            quantized_value = converted_value.magnitude.quantize(Decimal('1.000000'))
            self.data_box.setText(str(quantized_value))


class CheckBoxDataRow(QHBoxLayout):
    def __init__(self, label_string: str, read_only: bool) -> None:
        super().__init__(None)

        self.addWidget(QLabel(label_string))
        self.addStretch()

        self.check_box = QCheckBox()
        self.check_box.setDisabled(read_only)
        self.addWidget(self.check_box)


class ComboBoxDataRow(QHBoxLayout):
    def __init__(
            self,
            label_string: str,
            values: ComboBoxDataType | Iterable,
            read_only: bool,
    ) -> None:
        super().__init__(None)
        self.combo_box = QComboBox(None)

        self.addWidget(QLabel(label_string))
        self.addStretch()
        self.addWidget(self.combo_box)

        # Enforce read only
        self.combo_box.setDisabled(read_only)

        # Load the possible values into the combo box
        self._load_data(values)

    def _load_data(self, values: ComboBoxDataType | Iterable) -> None:
        # Handle if we got a simple iterable first
        if isinstance(values, Iterable):
            self.combo_box.addItems(values)
        elif isinstance(values, ComboBoxDataType):
            pass
        else:
            raise RuntimeError(f'Invalid type for "values": {type(values)}')
