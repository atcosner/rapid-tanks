from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QLineEdit, QTextEdit, QGridLayout, QPushButton,
)

from src.components.tank import Tank

from src.gui import RESOURCE_DIR


class TankInfoFrame(QFrame):
    def __init__(self, parent: QWidget, read_only: bool) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.read_only = read_only

        self.identifier = QLineEdit()
        self.description = QTextEdit()
        self.edit_button = QPushButton()

        self._initial_setup()

    def _initial_setup(self) -> None:
        # All the text widgets should match our read-only status
        self.identifier.setReadOnly(self.read_only)
        self.description.setReadOnly(self.read_only)

        # Set up the edit button
        # TODO: Open a tank edit window
        self.edit_button.setIcon(QIcon(str(RESOURCE_DIR / 'pencil.png')))
        self.edit_button.setMaximumSize(65, 65)

        # Layout the widgets
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Identifier
        main_layout.addWidget(QLabel('Identifier:' if self.read_only else 'Identifier (*):'), 0, 0)
        main_layout.addWidget(self.identifier, 0, 1)

        # Description
        main_layout.addWidget(QLabel('Description:'), 1, 0)
        main_layout.addWidget(self.description, 1, 1)

        if self.read_only:
            main_layout.addWidget(self.edit_button, 0, 2)
        else:
            main_layout.addWidget(QLabel('(*) = Required'), 3, 0)

    def load(self, tank: Tank) -> None:
        self.identifier.setText(tank.identifier)
        self.description.setText(tank.description)
