from PyQt5.QtWidgets import QWidget, QTabWidget, QMessageBox

from src.components.tank import Tank
from src.gui.widgets.tank.tank_info_frame import TankInfoFrame
from src.gui.widgets.tank.fixed_roof.vertical_physical_frame import VerticalPhysicalFrame


class TankTabWidget(QTabWidget):
    def __init__(self, parent: QWidget, read_only: bool) -> None:
        super().__init__(parent)

        # Widgets for each tab
        self.tank_info = TankInfoFrame(self, read_only=read_only)
        self.physical_properties = VerticalPhysicalFrame(self, read_only=False)

        self._initial_setup()

    def _initial_setup(self) -> None:
        self.addTab(self.tank_info, 'Identification')
        self.addTab(self.physical_properties, 'Physical Properties')

    def get_tank(self) -> Tank | None:
        # Check if the tank info has the required fields filled out
        info_result = self.tank_info.check()
        physical_result = self.physical_properties.check()

        # If we had errors, show the user an error dialog
        if not info_result.valid or not physical_result.valid:
            errors = '\n'.join(info_result.errors + physical_result.errors)
            QMessageBox.critical(self, 'Data Entry Errors', f'There are some errors with this tank:\n{errors}')
            return None

        # TODO: We need to handle different types of tanks

        # Create the tank object
        generic_tank = self.tank_info.build()
        tank = self.physical_properties.build()
        tank.identifier = generic_tank.identifier
        tank.description = generic_tank.description
        return tank
