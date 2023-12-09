from decimal import Decimal
from pint import Quantity

from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QCheckBox

from src.util.units import to_human_readable

from .validators import NonZeroDoubleValidator


class DataEntryLineEdit(QLineEdit):
    def __init__(self, read_only: bool) -> None:
        super().__init__()

        # Set some defaults
        self.setReadOnly(read_only)
        self.setMaximumWidth(100)
        self.setAlignment(QtCore.Qt.AlignRight)

        # Use the non-zero validator by default
        # TODO: Allow other types of validators since some quantities can be negative
        self.setValidator(NonZeroDoubleValidator())


class NumericDataRow(QHBoxLayout):
    def __init__(self, label_string: str, unit: str, read_only: bool = True) -> None:
        super().__init__(None)
        self.unit = unit

        self.label = QLabel(
            f'{label_string} ({to_human_readable(unit)})'
            if unit != 'dimensionless' else
            label_string
        )
        self.addWidget(self.label)

        self.addStretch()

        self.data_box = DataEntryLineEdit(read_only)
        self.addWidget(self.data_box)

    def set_text(self, value: Quantity | str) -> None:
        if isinstance(value, str):
            self.data_box.setText(value)
        else:
            # Convert to our unit
            converted_value = value.to(self.unit)

            # Limit to 6 decimal places
            quantized_value = converted_value.magnitude.quantize(Decimal('1.000000'))
            self.data_box.setText(str(quantized_value))


class CheckboxDataRow(QHBoxLayout):
    def __init__(self, label_string: str, read_only: bool) -> None:
        super().__init__(None)

        self.addWidget(QLabel(label_string))
        self.addStretch()

        self.check_box = QCheckBox()
        self.check_box.setDisabled(read_only)
        self.addWidget(self.check_box)
