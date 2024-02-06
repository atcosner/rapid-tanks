from PyQt5.QtWidgets import QMainWindow, QMessageBox

from src.data.data_library import DataLibrary
from src.gui.modals.facility_selector import FacilitySelector
from src.gui.widgets.facility.facility_tab_widget import FacilityTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        self.data_library = DataLibrary(preload=False)

        self.facility_tabs = FacilityTabWidget(self, self.data_library)

        self._initial_setup()
        self.show()

        self.select_facility(allow_new=True)

    def _initial_setup(self) -> None:
        # Ensure we are never shrunk too small
        self.setMinimumSize(600, 400)

        self.setWindowTitle('Rapid Tanks')
        self.setCentralWidget(self.facility_tabs)

        self._create_menubar()

        # TODO: Show a slash screen and preload the DB
        self.data_library.preload()

    def _create_menubar(self) -> None:
        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction('New Facility').triggered.connect(self.create_facility)
        file_menu.addAction('Open Facility').triggered.connect(lambda: self.select_facility(allow_new=False))
        file_menu.addSeparator()
        file_menu.addAction('Exit').triggered.connect(self.close)

        # # Create the menu for materials options
        # materials_menu = self.menuBar().addMenu('Materials')
        # materials_menu.addAction('Create Custom Material')
        # materials_menu.addSeparator()

    def create_facility(self) -> None:
        self.load_facility(self.data_library.create_facility().id)

    def select_facility(self, allow_new: bool) -> None:
        result = FacilitySelector.select_facility(self, allow_new=allow_new)

        if result == -1:
            # New Facility
            self.create_facility()
        elif result > 0:
            # Existing Facility - Result is the ID
            self.load_facility(result)

    def load_facility(self, facility_id: int) -> None:
        # Get the facility from the library
        facility = self.data_library.get_facility(facility_id)
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
