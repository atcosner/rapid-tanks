from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox,
)

from src.components.facility import Facility
from src.constants.meteorological import MeteorologicalSite
from src.data.facility_library import FacilityLibrary
from src.gui.widgets.dialog import Dialog
from src.gui.widgets.meteorological_data_frame import MeteorologicalDataFrame
from src.gui.widgets.meteorological_selection_frame import MeteorologicalSelectionFrame


class FacilityInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__(None)
        self._initial_setup()

    def _initial_setup(self) -> None:
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Facility Name
        layout_1 = QHBoxLayout()
        main_layout.addLayout(layout_1)

        layout_1.addWidget(QLabel('Name (*):'))
        self.facility_name = QLineEdit()
        layout_1.addWidget(self.facility_name)

        # Company
        layout_2 = QHBoxLayout()
        main_layout.addLayout(layout_2)

        layout_2.addWidget(QLabel('Company:'))
        self.company_name = QLineEdit()
        layout_2.addWidget(self.company_name)

        # Description
        layout_3 = QHBoxLayout()
        main_layout.addLayout(layout_3)

        layout_3.addWidget(QLabel('Description:'))
        self.description = QTextEdit()
        layout_3.addWidget(self.description)

    def check_and_build_facility(self) -> Facility | None:
        # Ensure the facility has a name
        if not self.facility_name.text():
            return None

        # Return a new facility
        return Facility(
            id=-1,  # This is set in the DB once the facility is inserted
            name=self.facility_name.text(),
            description=self.description.toPlainText(),
            company=self.company_name.text(),
        )


class MeteorologicalInfoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__(None)
        self._initial_setup()

    def _initial_setup(self) -> None:
        self.selection_frame = MeteorologicalSelectionFrame(self)
        self.data_frame = MeteorologicalDataFrame(self)

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

        self.facility_info = FacilityInfoWidget()
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
        if (facility := self.facility_info.check_and_build_facility()) is None:
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
