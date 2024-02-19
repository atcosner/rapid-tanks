from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit

from src.gui.widgets.util.validators import PositiveDoubleValidator, DoubleValidator
from src.util.units import to_human_readable

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

    def set(self, value: str) -> None:
        self.data_box.setText(value)

    def get(self) -> str:
        return self.data_box.text()
