from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit

from src.gui.widgets.util.validators import DoubleValidator, PositiveDoubleValidator


class DataEntryLineEdit(QLineEdit):
    def __init__(
            self,
            allow_negative: bool,
            precision: int,
    ) -> None:
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignRight)
        self.setMaximumWidth(75)

        # Set up the validator
        if allow_negative:
            self.setValidator(DoubleValidator(precision))
        else:
            self.setValidator(PositiveDoubleValidator(precision))
