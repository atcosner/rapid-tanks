import logging
from sqlalchemy.orm import Session

from PyQt5.Qt import pyqtSlot
from PyQt5.QtWidgets import QWidget, QTabWidget

from src.database import DB_ENGINE
from src.database.definitions.tank import FixedRoofTank
from src.gui.widgets.tank.tank_info_frame import TankInfoFrame
from src.gui.widgets.tank.tank_physical_frame import TankPhysicalFrame
from src.gui.widgets.tank.tank_usage_frame import TankUsageFrame

logger = logging.getLogger(__name__)


class TankTabWidget(QTabWidget):
    def __init__(
            self,
            parent: QWidget,
            read_only: bool,
    ) -> None:
        super().__init__(parent)

        self.tank_info = TankInfoFrame(self, start_read_only=read_only)
        self.tank_physical = TankPhysicalFrame(self, start_read_only=read_only)
        self.tank_usage = TankUsageFrame(self, start_read_only=read_only)

        self.current_tank_id: int | None = None

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addTab(self.tank_info, 'Identification')
        self.addTab(self.tank_physical, 'Physical Properties')
        self.addTab(self.tank_usage, 'Usage')

        # Start each widget disabled until we load a tank
        self.tank_info.setDisabled(True)
        self.tank_physical.setDisabled(True)
        self.tank_usage.setDisabled(True)

    def is_dirty(self) -> bool:
        # TODO: Include the active physical widget
        return self.tank_info.is_dirty() or self.tank_usage.is_dirty()

    @pyqtSlot(int)
    def load_tank(self, tank_id: int) -> None:
        self.current_tank_id = tank_id

        # Lookup the tank in the DB
        with Session(DB_ENGINE) as session:
            # TODO: Other types of tanks
            tank = session.get(FixedRoofTank, tank_id)
            self.tank_info.load(tank)
            self.tank_physical.load(tank)
            self.tank_usage.load(tank)

        # Enable the tabs
        self.tank_info.setDisabled(False)
        self.tank_physical.setDisabled(False)
        self.tank_usage.setDisabled(False)

    @pyqtSlot(int)
    def handle_tank_deleted(self, tank_id: int) -> None:
        if tank_id != self.current_tank_id:
            logger.info(f'Ignoring delete for tank {tank_id}, not currently displayed')
            return None

        self.current_tank_id = None

        self.tank_info.unload()
        self.tank_physical.unload()
        self.tank_usage.unload()
