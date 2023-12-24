from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from src.components.facility import Facility
from src.gui.widgets.util.data_entry_rows import TextLineDataRow, TextEditDataRow
from src.gui.widgets.util.editable_frame import EditableFrame


class FacilityInfoFrame(EditableFrame):
    def __init__(self, parent: QWidget, start_read_only: bool) -> None:
        super().__init__(parent)

        self.facility_name = self.register_control(TextLineDataRow('Name (*):', start_read_only))
        self.facility_company = self.register_control(TextLineDataRow('Company:', start_read_only))
        self.facility_description = self.register_control(TextEditDataRow('Description:', start_read_only))

        self.previous_facility: Facility | None = None

        if start_read_only:
            super().handle_end_editing()
        else:
            super().handle_begin_editing()

        # Register our edit handlers
        self.register_edit_handlers(
            begin_func=self.handle_begin_editing,
            end_close_func=lambda: self.handle_end_editing(False),
            end_save_func=lambda: self.handle_end_editing(True),
        )

        self._set_up_layout()

    def _set_up_layout(self) -> None:
        # Layout the widgets
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        facility_layout = QVBoxLayout()
        main_layout.addLayout(facility_layout)

        facility_layout.addWidget(self.facility_name)
        facility_layout.addWidget(self.facility_company)
        facility_layout.addWidget(self.facility_description)

        # Edit Buttons
        main_layout.addLayout(self.edit_button_layout)

    def load(self, facility: Facility) -> None:
        self.facility_name.set(facility.name)
        self.facility_company.set(facility.company)
        self.facility_description.set(facility.description)

    def get_facility(self, validate: bool = True) -> Facility | None:
        # Validate mandatory fields
        if validate:
            if not self.facility_name.get():
                return None

        # Return a new facility
        return Facility(
            id=-1,  # This is set in the DB once the facility is inserted
            name=self.facility_name.get(),
            description=self.facility_description.get(),
            company=self.facility_company.get(),
        )

    @pyqtSlot()
    def handle_begin_editing(self) -> None:
        super().handle_begin_editing()

        # Save the current state
        self.previous_facility = self.get_facility(validate=False)

    @pyqtSlot(bool)
    def handle_end_editing(self, save: bool) -> None:
        super().handle_end_editing()

        # Handle if we need to save the new data or reload the old data
        if save:
            # TODO: How do we handle this since we don't have a library?
            pass
        else:
            # If we cancel, reload the previous data
            self.load(self.previous_facility)
