from decimal import Decimal
from pint import Quantity

from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit


class DataRow(QHBoxLayout):
    def __init__(self, label_string: str, unit: str) -> None:
        super().__init__(None)
        self.unit = unit

        self.label = QLabel(label_string)
        self.addWidget(self.label)

        self.addStretch()

        self.text_box = QLineEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setMaximumWidth(150)
        self.text_box.setAlignment(QtCore.Qt.AlignRight)
        self.addWidget(self.text_box)

    def set_text(self, value: Quantity | str) -> None:
        if isinstance(value, str):
            self.text_box.setText(value)
        else:
            # Convert to our unit
            converted_value = value.to(self.unit)

            # Limit to 4 decimal places
            quantized_value = converted_value.magnitude.quantize(Decimal('1.0000'))
            self.text_box.setText(str(quantized_value))
