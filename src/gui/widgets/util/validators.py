from PyQt5.QtGui import QDoubleValidator


class DoubleValidator(QDoubleValidator):
    def __init__(self) -> None:
        super().__init__(None)
        self.setDecimals(6)


class NonZeroDoubleValidator(QDoubleValidator):
    def __init__(self) -> None:
        super().__init__(None)
        self.setBottom(0.0)
        self.setDecimals(6)
