from PyQt5.QtGui import QDoubleValidator


class DoubleValidator(QDoubleValidator):
    def __init__(self, precision: int) -> None:
        super().__init__(None)
        self.setDecimals(precision)


class PositiveDoubleValidator(QDoubleValidator):
    def __init__(self, precision: int) -> None:
        super().__init__(None)
        self.setBottom(0.0)
        self.setDecimals(precision)
