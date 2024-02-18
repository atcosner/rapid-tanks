from collections.abc import Iterable
from decimal import Decimal
from enum import Enum, auto
from pint import Quantity

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QTextEdit,
)

from src import unit_registry
from src.util.units import to_human_readable

from .validators import NonZeroDoubleValidator, DoubleValidator

DEFAULT_MARGINS = [2, 2, 2, 2]


class ComboBoxDataType(Enum):
    PAINT_COLORS = auto()
    PAINT_CONDITIONS = auto()


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
            self.setValidator(NonZeroDoubleValidator(precision))


class NumericDataRow(QWidget):
    def __init__(
            self,
            label_string: str,
            unit: str,
            read_only: bool,
            allow_negative: bool = False,
            default: str | None = '0.0',
            precision: int = 6,
    ) -> None:
        super().__init__(None)
        self.unit = unit
        self.precision = precision

        self.label = QLabel(
            f'{label_string} ({to_human_readable(unit)})'
            if unit != 'dimensionless' else
            label_string
        )
        self.data_box = DataEntryLineEdit(read_only, allow_negative, precision)

        # Set up our layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addStretch()
        main_layout.addWidget(self.data_box)
        self.setLayout(main_layout)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

        if default is not None:
            self.set(default)

    def set_read_only(self, read_only: bool) -> None:
        self.data_box.setReadOnly(read_only)

    def set(self, value: Quantity | str) -> None:
        if isinstance(value, str):
            self.data_box.setText(value)
        else:
            # Convert to our unit
            converted_value = value.to(self.unit)

            # Limit to our configured precision
            quantized_value = converted_value.magnitude.quantize(Decimal(f'1.{"0" * self.precision}'))
            self.data_box.setText(str(quantized_value))

    def get(self) -> Quantity:
        # TODO: How should we handle errors in the conversion?
        string_value = self.data_box.text()
        return unit_registry.Quantity(Decimal(string_value), self.unit)


class CheckBoxDataRow(QWidget):
    def __init__(self, label_string: str, read_only: bool) -> None:
        super().__init__(None)
        self.check_box = QCheckBox()
        self.check_box.setDisabled(read_only)

        # Set up our layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QLabel(label_string))
        main_layout.addStretch()
        main_layout.addWidget(self.check_box)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)


class ComboBoxDataRow(QWidget):
    selectionChanged = pyqtSignal(str)

    def __init__(
            self,
            label_string: str,
            values: ComboBoxDataType | Iterable,
            read_only: bool,
    ) -> None:
        super().__init__(None)
        self.combo_box = QComboBox(None)
        self.combo_box.currentTextChanged.connect(self.selectionChanged)

        # Set up our layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QLabel(label_string))
        main_layout.addStretch()
        main_layout.addWidget(self.combo_box)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

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

    def get_selected(self) -> str:
        return self.combo_box.currentText()


class TextLineDataRow(QWidget):
    def __init__(
            self,
            label_string: str,
            read_only: bool,
            no_stretch: bool = True,
    ) -> None:
        super().__init__(None)

        self.label = QLabel(label_string)
        self.data_box = QLineEdit()

        self.data_box.setReadOnly(read_only)

        # Set up our layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label)

        if not no_stretch:
            main_layout.addStretch()

        main_layout.addWidget(self.data_box)
        self.setLayout(main_layout)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.data_box.setReadOnly(read_only)

    def set(self, value: str) -> None:
        self.data_box.setText(value)

    def get(self) -> str:
        return self.data_box.text()


class TextEditDataRow(QWidget):
    def __init__(
            self,
            label_string: str,
            read_only: bool,
            no_stretch: bool = True,
    ) -> None:
        super().__init__(None)

        self.label = QLabel(label_string)
        self.data_box = QTextEdit()

        self.data_box.setReadOnly(read_only)

        # Set up our layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label)

        if not no_stretch:
            main_layout.addStretch()

        main_layout.addWidget(self.data_box)
        self.setLayout(main_layout)

        main_layout.setContentsMargins(*DEFAULT_MARGINS)

    def set_read_only(self, read_only: bool) -> None:
        self.data_box.setReadOnly(read_only)

    def set(self, value: str) -> None:
        self.data_box.setText(value)

    def get(self) -> str:
        return self.data_box.toPlainText()
