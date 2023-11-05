from enum import IntEnum

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QDialog, QRadioButton, QVBoxLayout, QFrame, QButtonGroup, QHBoxLayout, QLabel, QListWidget,
    QPushButton,
)

from ..widgets.search_bar import SearchBar


class FacilitySelection(IntEnum):
    NEW = 1
    EXISTING = 2


class FacilitySelector(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Facility Selector')

        # Disable the help button on the title bar
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        # Ensure we don't get shrunk too much
        self.setMinimumWidth(250)

        self._initial_setup()

    def _initial_setup(self) -> None:
        main_layout = QVBoxLayout()

        button_group = QButtonGroup(self)
        button_group.idClicked.connect(self.handle_button_group_change)

        # New Facility
        new_facility_layout = QVBoxLayout()

        new_facility_button = QRadioButton('Create a new Facility')
        button_group.addButton(new_facility_button, FacilitySelection.NEW)
        new_facility_layout.addWidget(new_facility_button)

        main_layout.addLayout(new_facility_layout)

        # 'Or' Label
        label_layout = QHBoxLayout()
        label_layout.addStretch()
        label_layout.addWidget(QLabel('- Or -'))
        label_layout.addStretch()
        main_layout.addLayout(label_layout)

        # Existing Facility
        existing_facility_button = QRadioButton('Open an existing Facility')
        button_group.addButton(existing_facility_button, FacilitySelection.EXISTING)
        main_layout.addWidget(existing_facility_button)

        self.existing_facility_frame = QFrame(self)
        self.existing_facility_frame.setFrameStyle(QFrame.Box)

        existing_facility_layout = QVBoxLayout()
        self.existing_facility_frame.setLayout(existing_facility_layout)

        search_bar = SearchBar()
        existing_facility_layout.addWidget(search_bar)

        self.facility_list = QListWidget(self)
        existing_facility_layout.addWidget(self.facility_list)

        main_layout.addWidget(self.existing_facility_frame)

        # Exit Buttons
        exit_button_layout = QHBoxLayout()
        ok_button = QPushButton('OK')
        cancel_button = QPushButton('Cancel')
        cancel_button.pressed.connect(self.hide)

        exit_button_layout.addWidget(ok_button)
        exit_button_layout.addWidget(cancel_button)
        main_layout.addLayout(exit_button_layout)

        self.setLayout(main_layout)

    @pyqtSlot(int)
    def handle_button_group_change(self, id: int) -> None:
        facility_selection = FacilitySelection(id)
        if facility_selection is FacilitySelection.NEW:
            self.existing_facility_frame.setDisabled(True)
        elif facility_selection is FacilitySelection.EXISTING:
            self.existing_facility_frame.setDisabled(False)

    def exec(self) -> None:
        # Load up the item list before we show ourselves

        # Set a default checked state based on if we have any existing facilities or not

        super().exec()
