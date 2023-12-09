from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
)

from src.constants.meteorological import MeteorologicalSite
from src.data.facility_library import FacilityLibrary
from src.gui.widgets.util.dialog import Dialog
from src.gui.widgets.facility.facility_info_frame import FacilityInfoFrame
from src.gui.widgets.meteorological.meteorological_info_frame import MeteorologicalInfoFrame
from src.gui.widgets.meteorological.meteorological_selection_frame import MeteorologicalSelectionFrame


class MeteorologicalInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__(None)
        self._initial_setup()

    def _initial_setup(self) -> None:
        self.selection_frame = MeteorologicalSelectionFrame(self)
        self.data_frame = MeteorologicalInfoFrame(self)

        self.selection_frame.siteSelected.connect(self.data_frame.handle_site_selected)

        layout = QHBoxLayout()
        layout.addWidget(self.selection_frame)
        layout.addWidget(self.data_frame)
        self.setLayout(layout)

    def get_site(self) -> MeteorologicalSite | None:
        return self.selection_frame.get_selected_site()


class FacilityCreator(Dialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.library = FacilityLibrary()
        self._initial_setup()

    def _initial_setup(self) -> None:
        self.setWindowTitle('Facility Creator')

        tab_widget = QTabWidget(self)

        self.facility_info = FacilityInfoFrame(self, read_only=False)
        tab_widget.addTab(self.facility_info, 'Facility Info')

        self.meteorological_info = MeteorologicalInfoWidget()
        tab_widget.addTab(self.meteorological_info, 'Meteorological Info')

        # Exit Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton('Save')
        save_button.pressed.connect(self.check_and_save_facility)

        cancel_button = QPushButton('Cancel')
        cancel_button.pressed.connect(self.reject)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    @pyqtSlot()
    def check_and_save_facility(self) -> None:
        # See if the facility info is filled out enough
        if (facility := self.facility_info.get_facility()) is None:
            return QMessageBox.critical(self, 'Form Error', 'Please fill out all mandatory fields (*)')
        if (meteorological_site := self.meteorological_info.get_site()) is None:
            return QMessageBox.critical(self, 'Form Error', 'Please choose a valid meteorological site')

        # Insert the facility into the DB
        facility.meteorological_data = meteorological_site
        self.done(self.library.store(facility))

    @classmethod
    def create_facility(cls, parent: QWidget) -> int:
        dialog = cls(parent)
        return dialog.exec()
