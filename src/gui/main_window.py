from PyQt5.QtWidgets import QMainWindow, QDialog

from src.gui.modals.facility_selector import FacilitySelector
from src.gui.modals.material_library import MaterialLibrary


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)

        # Child windows/dialogs
        self.facility_selector = FacilitySelector(self)
        #self.material_library = MaterialLibrary(self)

        self._initial_setup()
        self.show()

        self.select_facility()

    def _initial_setup(self) -> None:
        self.setWindowTitle('Rapid Tanks | Version 0.1')

        # Ensure we are never shrunk too small
        self.setMinimumSize(600, 400)

        self._create_menubar()

    def _create_menubar(self) -> None:
        file_menu = self.menuBar().addMenu('File')
        file_menu.addSeparator()
        file_menu.addAction('Exit').triggered.connect(self.close)

        # Create the menu to add new components
        add_menu = self.menuBar().addMenu('Add')
        add_menu.addAction('New Tank')

        # Create the menu for materials options
        materials_menu = self.menuBar().addMenu('Materials')
        materials_menu.addAction('Create Custom Material')
        materials_menu.addSeparator()
       # materials_menu.addAction('Materials Library').triggered.connect(self.material_library.show)

    def select_facility(self) -> None:
        # Show the facility selection dialog
        result = self.facility_selector.exec()
        if result == -1:
            # New Facility
            # TODO: Show site creation dialog
            pass
        elif result > 0:
            # Existing Facility - Result is the ID
            self.load_facility(result)

    def load_facility(self, facility_id: int) -> None:
        pass