from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtCore import QObject, QEvent, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QMessageBox

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.gui.widgets.facility.facility_info_frame import FacilityInfoFrame
from src.gui.widgets.facility.facility_meteorological_frame import FacilityMeteorologicalFrame
from src.gui.widgets.facility.facility_tanks_frame import FacilityTanksFrame


class FacilityTabWidget(QTabWidget):
    def __init__(
            self,
            parent: QWidget,
    ) -> None:
        super().__init__(parent)

        self.current_facility_id: int | None = None

        # Widgets for each tab
        self.facility_info = FacilityInfoFrame(self, start_read_only=True)
        self.facility_meteorological_info = FacilityMeteorologicalFrame(self)
        self.tanks_info = FacilityTanksFrame(self)

        # Connect signals
        self.facility_info.facilityInfoChanged.connect(self.handle_update_facility_info)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addTab(self.facility_info, 'Facility Info')
        self.addTab(self.facility_meteorological_info, 'Meteorological')
        self.addTab(self.tanks_info, 'Tanks')

        # Install the event filter
        self.installEventFilter(self)
        self.tabBar().installEventFilter(self)

    def load(self, facility: Facility) -> None:
        self.current_facility_id = facility.id

        self.facility_info.load(facility)
        self.facility_meteorological_info.load(facility)
        self.tanks_info.load(facility)

    @pyqtSlot(int)
    def handle_update_facility_info(self, facility_id: int) -> None:
        assert facility_id == self.current_facility_id, \
            f'Updating a facility not currently loaded! Current: {self.current_facility_id}, New: {facility_id}'

        # Update the title of our parent
        with Session(DB_ENGINE) as session:
            facility = session.get(Facility, facility_id)
            self.parent().setWindowTitle(f'Rapid Tanks | {facility.name}')

    def can_change_tab(self) -> bool:
        if self.currentWidget().is_dirty():
            # Alert the user and stop the tab change
            QTimer.singleShot(
                0,
                lambda: QMessageBox.warning(
                    self,
                    'Unsaved Changes',
                    'Please save or cancel editing before changing tabs',
                ),
            )
            return True
        else:
            # Not dirty, which could mean an edit with no changes so end editing before we change
            if self.currentWidget().edit_in_progress:
                self.currentWidget().handle_end_editing(save=False)

        return False

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        # Before we accept an event that could change tabs, ensure the current tab is not dirty
        if (event.type() == event.KeyPress
            and event.key() in (Qt.Key_Left, Qt.Key_Right)
        ):
            return self.can_change_tab()
        elif (source == self.tabBar()
              and event.type() == event.MouseButtonPress
              and event.button() == Qt.LeftButton
        ):
            tab = self.tabBar().tabAt(event.pos())
            if tab >= 0 and tab != self.currentIndex():
                return self.can_change_tab()
        elif (source == self
              and event.type() == event.KeyPress
              and event.key() in (Qt.Key_Tab, Qt.Key_Backtab)
              and event.modifiers() & Qt.ControlModifier
        ):
            return self.can_change_tab()

        return super().eventFilter(source, event)
