from PyQt5.QtWidgets import (
    QWidget, QFrame, QLabel, QLineEdit, QTextEdit, QGridLayout,
)


class FacilityInfoFrame(QFrame):
    def __init__(self, parent: QWidget, read_only: bool) -> None:
        super().__init__(parent)
        self.setFrameStyle(QFrame.Box)

        self.read_only = read_only

        self.facility_name = QLineEdit()
        self.facility_company = QLineEdit()
        self.facility_description = QTextEdit()

        self._initial_setup()

    def _initial_setup(self) -> None:
        # All the text widgets should be read-only if we are
        if self.read_only:
            self.facility_name.setDisabled(True)
            self.facility_company.setDisabled(True)
            self.facility_description.setDisabled(True)

        # Layout the widgets
        main_layout = QGridLayout()
        self.setLayout(main_layout)

        # Facility Name
        main_layout.addWidget(QLabel('Name:'), 0, 0)
        main_layout.addWidget(self.facility_name, 0, 1)

        # Company
        main_layout.addWidget(QLabel('Company:'), 1, 0)
        main_layout.addWidget(self.facility_company, 1, 1)

        # Description
        main_layout.addWidget(QLabel('Description:'), 2, 0)
        main_layout.addWidget(self.facility_description, 2, 1)
