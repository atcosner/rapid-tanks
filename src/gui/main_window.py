from PyQt5.QtWidgets import QMainWindow, QMessageBox

from src.data.facility_library import FacilityLibrary
from src.gui.modals.facility_dialogs import FacilitySelector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        self._initial_setup()
        self.show()

        self.select_facility(allow_new=True)

    def _initial_setup(self) -> None:
        self.setWindowTitle('Rapid Tanks | Version 0.1')

        # Ensure we are never shrunk too small
        self.setMinimumSize(600, 400)

        self._create_menubar()

    def _create_menubar(self) -> None:
        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction('New Site')
        file_menu.addAction('Open Site').triggered.connect(lambda: self.select_facility(allow_new=False))
        file_menu.addAction('Save')
        file_menu.addSeparator()
        file_menu.addAction('Exit').triggered.connect(self.close)

        # Create the menu to add new components
        add_menu = self.menuBar().addMenu('Add')
        add_menu.addAction('New Tank')

        # Create the menu for materials options
        materials_menu = self.menuBar().addMenu('Materials')
        materials_menu.addAction('Create Custom Material')
        materials_menu.addSeparator()

    def select_facility(self, allow_new: bool) -> None:
        # Show the startup facility selection dialog
        result = FacilitySelector.select_facility(self, allow_new=allow_new)
        if result == -1:
            # New Facility
            # TODO: Show site creation dialog
            pass
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

        # TODO: Load something?
