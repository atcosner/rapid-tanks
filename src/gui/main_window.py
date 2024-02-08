from datetime import datetime
from sqlalchemy.orm import Session

from PyQt5.QtWidgets import QMainWindow, QMessageBox

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.gui.modals.facility_selector import FacilitySelector
from src.gui.widgets.facility.facility_tab_widget import FacilityTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.facility_tabs = FacilityTabWidget(self)

        # TODO: Show a slash screen and do any long running operations

        self._initial_setup()
        self.show()

        self.select_facility(allow_new=True)

    def _initial_setup(self) -> None:
        # Ensure we are never shrunk too small
        self.setMinimumSize(600, 400)

        self.setWindowTitle('Rapid Tanks')
        self.setCentralWidget(self.facility_tabs)

        self._create_menubar()

    def _create_menubar(self) -> None:
        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction('New Facility').triggered.connect(lambda: self.load_facility(facility_id=None))
        file_menu.addAction('Open Facility').triggered.connect(lambda: self.select_facility(allow_new=False))
        file_menu.addSeparator()
        file_menu.addAction('Exit').triggered.connect(self.close)

        # # Create the menu for materials options
        # materials_menu = self.menuBar().addMenu('Materials')
        # materials_menu.addAction('Create Custom Material')
        # materials_menu.addSeparator()

    def select_facility(self, allow_new: bool) -> None:
        result = FacilitySelector.select_facility(self, allow_new=allow_new)
        self.load_facility(result if result else None)

    def load_facility(self, facility_id: int | None) -> None:
        # Load the facility
        with Session(DB_ENGINE) as session:
            if facility_id:
                facility = session.get(Facility, facility_id)
                if facility is None:
                    return QMessageBox.critical(
                        self,
                        'Load Facility Error',
                        f'Could not load facility!\nID {facility_id} did not exist.',
                    )
            else:
                facility = Facility(name='New Facility', description=f'Created {datetime.now():%d/%m/%y %H:%M:%S}')
                session.add(facility)
                session.commit()

            # Change our title
            self.setWindowTitle(f'Rapid Tanks | {facility.name}')

            # Load the facility
            self.facility_tabs.load(facility)
