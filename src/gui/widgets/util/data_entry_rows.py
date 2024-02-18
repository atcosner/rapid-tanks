from decimal import Decimal
from pint import Quantity

from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QTextEdit,
)

from src.util.units import to_human_readable

from .validators import NonZeroDoubleValidator, DoubleValidator

DEFAULT_MARGINS = [2, 2, 2, 2]


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

    def get(self) -> str:
        # TODO: Would this be better as a quantity?
        return self.data_box.text()


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

    def set(self, value: bool) -> None:
        self.check_box.setChecked(value)

    def get(self) -> bool:
        return self.check_box.isChecked()


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
