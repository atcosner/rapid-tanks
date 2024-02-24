import logging
from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QTabWidget, QMessageBox

from src.components.tank import Tank
from src.database import DB_ENGINE
from src.database.definitions.tank import FixedRoofTank
from src.gui.widgets.tank.fixed_roof.vertical_physical_frame import VerticalPhysicalFrame
from src.gui.widgets.tank.tank_info_frame import TankInfoFrame
from src.gui.widgets.tank.tank_usage_frame import TankUsageFrame

logger = logging.getLogger(__name__)


class TankTabWidget(QTabWidget):
    def __init__(
            self,
            parent: QWidget,
            read_only: bool,
    ) -> None:
        super().__init__(parent)

        # Widgets for each tab
        self.tank_info = TankInfoFrame(self, start_read_only=read_only)
        self.physical_properties = VerticalPhysicalFrame(self, start_read_only=read_only)
        self.tank_usage = TankUsageFrame(self, start_read_only=read_only)

        self.current_tank_id: int | None = None

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addTab(self.tank_info, 'Identification')
        self.addTab(self.physical_properties, 'Physical Properties')
        self.addTab(self.tank_usage, 'Usage')

        # Start each widget disabled until we load a tank
        self.tank_info.setDisabled(True)
        self.physical_properties.setDisabled(True)
        self.tank_usage.setDisabled(True)

    def is_dirty(self) -> bool:
        return self.tank_info.is_dirty() or self.tank_usage.is_dirty()

    @pyqtSlot(int)
    def load_tank(self, tank_id: int) -> None:
        self.current_tank_id = tank_id

        # Lookup the tank in the DB
        with Session(DB_ENGINE) as session:
            # TODO: Other types of tanks
            tank = session.get(FixedRoofTank, tank_id)
            self.tank_info.load(tank)
            self.physical_properties.load(tank)
            self.tank_usage.load(tank)

            # TODO: Load the usage frame

        # Enable the tabs
        self.tank_info.setDisabled(False)
        self.physical_properties.setDisabled(False)
        self.tank_usage.setDisabled(False)

    @pyqtSlot(int)
    def handle_tank_deleted(self, tank_id: int) -> None:
        if tank_id != self.current_tank_id:
            logger.info(f'Ignoring delete for tank {tank_id}, not currently displayed')
            return None

        self.current_tank_id = None

        self.tank_info.unload()
        self.physical_properties.unload()
        self.tank_usage.unload()
