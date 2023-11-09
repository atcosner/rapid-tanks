from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QDialog


class Dialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Disable the help button on the title bar
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        # Ensure we don't get shrunk too much
        self.setMinimumWidth(250)
