from PyQt5.QtWidgets import QMainWindow, QMessageBox

from src.data.facility_library import FacilityLibrary
from src.gui.modals.facility_creator import FacilityCreator
from src.gui.modals.facility_selector import FacilitySelector
from src.gui.modals.tank_editor import TankEditor
from src.gui.widgets.facility.facility_tab_widget import FacilityTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        self.facility_tabs = FacilityTabWidget(self)

        self._initial_setup()
        self.show()

        self.select_facility(allow_new=True)

    def _initial_setup(self) -> None:
        self.setWindowTitle('Rapid Tanks | Version 0.1')

        # Ensure we are never shrunk too small
        self.setMinimumSize(600, 400)

        self._create_menubar()
        self.setCentralWidget(self.facility_tabs)

    def _create_menubar(self) -> None:
        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction('New Site').triggered.connect(self.create_facility)
        file_menu.addAction('Open Site').triggered.connect(lambda: self.select_facility(allow_new=False))
        file_menu.addAction('Save')
        file_menu.addSeparator()
        file_menu.addAction('Exit').triggered.connect(self.close)

        # Create the menu to add new components
        add_menu = self.menuBar().addMenu('Add')
        add_menu.addAction('New Tank').triggered.connect(self.create_tank)

        # Create the menu for materials options
        materials_menu = self.menuBar().addMenu('Materials')
        materials_menu.addAction('Create Custom Material')
        materials_menu.addSeparator()

    def create_facility(self) -> None:
        result = FacilityCreator.create_facility(self)

        # 0 = Canceled, > 0: Facility ID
        if result > 0:
            self.load_facility(result)

    def select_facility(self, allow_new: bool) -> None:
        # Show the startup facility selection dialog
        result = FacilitySelector.select_facility(self, allow_new=allow_new)
        if result == -1:
            # New Facility
            self.create_facility()
        elif result > 0:
            # Existing Facility - Result is the ID
            self.load_facility(result)

    def load_facility(self, facility_id: int) -> None:
        # Get the facility from the library
        facility = FacilityLibrary().get_facility_by_id(facility_id)
        if facility is None:
            return QMessageBox.critical(
                self,
                'Load Facility Error',
                f'Could not load facility!\nID {facility_id} did not exist.',
            )

        # Change our title
        self.setWindowTitle(f'Rapid Tanks | {facility.name}')

        # Load the facility
        self.facility_tabs.load(facility)

    def create_tank(self) -> None:
        TankEditor.create_tank(self)
