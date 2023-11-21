from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QLineEdit, QTextEdit, QGridLayout, QPushButton,
)

from src.components.facility import Facility

from .. import RESOURCE_DIR


class FacilityInfoFrame(QFrame):
    def __init__(self, parent: QWidget, read_only: bool) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.read_only = read_only

        self.facility_name = QLineEdit()
        self.facility_company = QLineEdit()
        self.facility_description = QTextEdit()
        self.edit_button = QPushButton()

        self._initial_setup()

    def _initial_setup(self) -> None:
        # Start in a disabled state
        self.setDisabled(True)

        # All the text widgets should match our read-only status
        self.facility_name.setReadOnly(self.read_only)
        self.facility_company.setReadOnly(self.read_only)
        self.facility_description.setReadOnly(self.read_only)

        # Set up the edit button
        # TODO: Open a facility edit window
        self.edit_button.setIcon(QIcon(str(RESOURCE_DIR / 'pencil.png')))
        self.edit_button.setMaximumSize(65, 65)

        # Layout the widgets
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Facility Name
        main_layout.addWidget(QLabel('Name:' if self.read_only else 'Name (*):'), 0, 0)
        main_layout.addWidget(self.facility_name, 0, 1)

        # Company
        main_layout.addWidget(QLabel('Company:'), 1, 0)
        main_layout.addWidget(self.facility_company, 1, 1)

        # Description
        main_layout.addWidget(QLabel('Description:'), 2, 0)
        main_layout.addWidget(self.facility_description, 2, 1)

        if self.read_only:
            main_layout.addWidget(self.edit_button, 0, 2)
        else:
            main_layout.addWidget(QLabel('(*) = Mandatory Fields'), 3, 0)

    def load(self, facility: Facility) -> None:
        self.facility_name.setText(facility.name)
        self.facility_company.setText(facility.company)
        self.facility_description.setText(facility.description)

        # Enable all the widgets
        self.setEnabled(True)

    def get_facility(self) -> Facility | None:
        # Validate mandatory fields
        if not self.facility_name.text():
            return None

        # Return a new facility
        return Facility(
            id=-1,  # This is set in the DB once the facility is inserted
            name=self.facility_name.text(),
            description=self.facility_description.toPlainText(),
            company=self.facility_company.text(),
        )
