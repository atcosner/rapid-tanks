from enum import IntEnum

from PyQt5 import QtCore
from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QDialog, QRadioButton, QVBoxLayout, QFrame, QButtonGroup, QHBoxLayout, QLabel, QListWidget,
    QPushButton, QListWidgetItem, QMessageBox,
)

from src.components.facility import Facility
from src.data.facility_library import FacilityLibrary

from ..widgets.search_bar import SearchBar


class FacilitySelection(IntEnum):
    NEW = 1
    EXISTING = 2


class FacilityListItem(QListWidgetItem):
    def __init__(self, facility: Facility) -> None:
        super().__init__(facility.name)
        self.facility = facility

    def get_id(self) -> int:
        return self.facility.id


class FacilitySelector(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Facility Selector')

        self.library = FacilityLibrary()

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

        self.new_facility_button = QRadioButton('Create a new Facility')
        button_group.addButton(self.new_facility_button, FacilitySelection.NEW)
        new_facility_layout.addWidget(self.new_facility_button)

        main_layout.addLayout(new_facility_layout)

        # 'Or' Label
        label_layout = QHBoxLayout()
        label_layout.addStretch()
        label_layout.addWidget(QLabel('- Or -'))
        label_layout.addStretch()
        main_layout.addLayout(label_layout)

        # Existing Facility
        self.existing_facility_button = QRadioButton('Open an existing Facility')
        button_group.addButton(self.existing_facility_button, FacilitySelection.EXISTING)
        main_layout.addWidget(self.existing_facility_button)

        self.existing_facility_frame = QFrame(self)
        self.existing_facility_frame.setFrameStyle(QFrame.Box)

        existing_facility_layout = QVBoxLayout()
        self.existing_facility_frame.setLayout(existing_facility_layout)

        search_bar = SearchBar()
        search_bar.textChanged.connect(self.handle_search)
        existing_facility_layout.addWidget(search_bar)

        self.facility_list = QListWidget(self)
        existing_facility_layout.addWidget(self.facility_list)

        main_layout.addWidget(self.existing_facility_frame)

        # Exit Buttons
        exit_button_layout = QHBoxLayout()
        ok_button = QPushButton('OK')
        ok_button.pressed.connect(lambda: self.handle_dialog_close())
        cancel_button = QPushButton('Cancel')
        cancel_button.pressed.connect(self.reject)

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

    def handle_dialog_close(self) -> None:
        # Return an integer depending on if the user selected new vs existing site
        if self.new_facility_button.isChecked():
            self.done(-1)
        else:
            current_item = self.facility_list.currentItem()
            if current_item.isHidden():
                QMessageBox.critical(self, 'Selection Error', 'Please select a facility')
            else:
                self.done(current_item.get_id())

    @pyqtSlot(str)
    def handle_search(self, search_text: str) -> None:
        for idx in range(self.facility_list.count()):
            facility_item = self.facility_list.item(idx)
            if not search_text or search_text in facility_item.text():
                facility_item.setHidden(False)
            else:
                facility_item.setHidden(True)

    def exec(self) -> int:
        # Enable controls that could be disabled from a previous iteration
        self.existing_facility_button.setDisabled(False)
        self.existing_facility_frame.setDisabled(False)

        # Clear existing entries and reload the facilities
        self.facility_list.clear()
        self.library.reload()

        # Load up the item list before we show ourselves
        for facility in self.library.facilities.values():
            self.facility_list.addItem(FacilityListItem(facility))

        # Set a default checked state based on if we have any existing facilities or not
        if self.facility_list.count() > 0:
            self.facility_list.setCurrentRow(0)
            self.existing_facility_button.setChecked(True)
        else:
            self.new_facility_button.setChecked(True)
            self.existing_facility_button.setDisabled(True)
            self.existing_facility_frame.setDisabled(True)

        return super().exec()
