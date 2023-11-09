from enum import IntEnum

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QRadioButton, QVBoxLayout, QButtonGroup, QHBoxLayout, QLabel, QPushButton, QMessageBox,
)

from ..widgets.dialog import Dialog
from ..widgets.facility_selection_frame import FacilitySelectionFrame


class FacilitySelection(IntEnum):
    NEW = 1
    EXISTING = 2


class FacilitySelector(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle('Facility Selector')

        # Widgets
        self.new_facility_button = QRadioButton('Create a new Facility')
        self.existing_facility_button = QRadioButton('Open an existing Facility')
        self.existing_facility_frame = FacilitySelectionFrame(self)

        self.exit_buttons_layout = QHBoxLayout()

        ok_button = QPushButton('OK')
        ok_button.pressed.connect(lambda: self.handle_dialog_close())
        self.exit_buttons_layout.addWidget(ok_button)

        cancel_button = QPushButton('Cancel')
        cancel_button.pressed.connect(self.reject)
        self.exit_buttons_layout.addWidget(cancel_button)

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
            selected_facility = self.existing_facility_frame.get_selected_facility()
            if selected_facility is None:
                return QMessageBox.critical(self, 'Selection Error', 'Please select a facility')
            else:
                self.done(selected_facility.id)

    def _initial_new_and_existing_setup(self) -> None:
        main_layout = QVBoxLayout()

        # Set up the button group
        button_group = QButtonGroup(self)
        button_group.idClicked.connect(self.handle_button_group_change)
        button_group.addButton(self.new_facility_button, FacilitySelection.NEW)
        button_group.addButton(self.existing_facility_button, FacilitySelection.EXISTING)

        # New Facility
        main_layout.addWidget(self.new_facility_button)

        # 'Or' Label
        label_layout = QHBoxLayout()
        label_layout.addStretch()
        label_layout.addWidget(QLabel('- Or -'))
        label_layout.addStretch()
        main_layout.addLayout(label_layout)

        # Existing Facility
        main_layout.addWidget(self.existing_facility_button)
        main_layout.addWidget(self.existing_facility_frame)

        # Exit Buttons
        main_layout.addLayout(self.exit_buttons_layout)

        self.setLayout(main_layout)

        # Set a default checked state based on if we have any existing facilities or not
        if self.existing_facility_frame.get_facility_count() > 0:
            self.existing_facility_button.setChecked(True)
        else:
            self.new_facility_button.setChecked(True)

            # Disable the existing facility frame since we didn't load anything
            self.existing_facility_button.setDisabled(True)
            self.existing_facility_frame.setDisabled(True)

    def _initial_existing_setup(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.existing_facility_frame)
        main_layout.addLayout(self.exit_buttons_layout)
        self.setLayout(main_layout)

    @classmethod
    def select_facility(cls, parent: QWidget, allow_new: bool) -> int:
        dialog = cls(parent)
        if allow_new:
            dialog._initial_new_and_existing_setup()
        else:
            dialog._initial_existing_setup()
        return dialog.exec()
