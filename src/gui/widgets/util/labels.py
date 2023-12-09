from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


class SubSectionHeader(QLabel):
    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setStyleSheet("QLabel { font: bold; color : deepskyblue; }")
