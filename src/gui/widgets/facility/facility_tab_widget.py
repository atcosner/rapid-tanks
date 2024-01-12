from PyQt5.QtWidgets import QWidget, QTabWidget

from src.components.facility import Facility
from src.gui.widgets.facility.facility_info_frame import FacilityInfoFrame
from src.gui.widgets.facility.facility_meteorological_frame import FacilityMeteorologicalFrame
from src.gui.widgets.facility.facility_tanks_frame import FacilityTanksFrame


class FacilityTabWidget(QTabWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Widgets for each tab
        self.facility_info = FacilityInfoFrame(self, start_read_only=True)
        self.facility_meteorological_info = FacilityMeteorologicalFrame(self)
        self.tanks_info = FacilityTanksFrame(self)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addTab(self.facility_info, 'Facility Info')
        self.addTab(self.facility_meteorological_info, 'Meteorological')
        self.addTab(self.tanks_info, 'Tanks')

    def load(self, facility: Facility) -> None:
        self.facility_info.load(facility)
        self.facility_meteorological_info.load(facility.meteorological_data)
