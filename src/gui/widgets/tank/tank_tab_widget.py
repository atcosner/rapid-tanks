from PyQt5.QtWidgets import QWidget, QTabWidget

from src.gui.widgets.tank.tank_info_frame import TankInfoFrame
from src.gui.widgets.tank.tank_physical_frame import TankPhysicalFrame


class TankTabWidget(QTabWidget):
    def __init__(self, parent: QWidget, read_only: bool) -> None:
        super().__init__(parent)

        # Widgets for each tab
        self.tank_info = TankInfoFrame(self, read_only=read_only)
        self.physical_properties = TankPhysicalFrame(self, read_only=False)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addTab(self.tank_info, 'Identification')
        self.addTab(self.physical_properties, 'Physical Properties')
