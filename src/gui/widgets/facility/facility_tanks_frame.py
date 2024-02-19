from PyQt5.QtWidgets import QWidget, QSplitter

from src.database.definitions.facility import Facility
from src.gui.widgets.tank.tank_selection_frame import TankSelectionFrame
from src.gui.widgets.tank.tank_tab_widget import TankTabWidget


class FacilityTanksFrame(QSplitter):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        # Widgets
        self.tank_select = TankSelectionFrame(self)
        self.tank_tabs = TankTabWidget(self, read_only=True)

        self.tank_select.tankSelected.connect(self.tank_tabs.load_tank)
        self.tank_select.tankDeleted.connect(self.tank_tabs.handle_tank_deleted)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addWidget(self.tank_select)
        self.addWidget(self.tank_tabs)

    def load(self, facility: Facility) -> None:
        self.tank_select.load(facility)
