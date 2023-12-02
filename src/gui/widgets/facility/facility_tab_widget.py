from PyQt5.QtWidgets import QWidget, QTabWidget

from src.components.facility import Facility
from src.gui.widgets.facility.facility_info_frame import FacilityInfoFrame


class FacilityTabWidget(QTabWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Widgets for each tab
        self.facility_info = FacilityInfoFrame(self, read_only=True)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addTab(self.facility_info, 'Facility Info')

    def load(self, facility: Facility) -> None:
        self.facility_info.load(facility)
