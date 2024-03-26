from PyQt5.QtWidgets import QWidget, QVBoxLayout

from src.database.definitions.fixed_roof_tank import FixedRoofTank
from src.gui.widgets.tank.fixed_roof.horizontal_physical_frame import HorizontalPhysicalFrame
from src.gui.widgets.tank.fixed_roof.vertical_physical_frame import VerticalPhysicalFrame
from src.util.enums import TankType


class TankPhysicalFrame(QWidget):
    def __init__(self, parent: QWidget, start_read_only: bool) -> None:
        super().__init__(parent)
        self.current_tank_type: TankType | None = TankType.VERTICAL_FIXED_ROOF

        self.physical_frames = {
            TankType.HORIZONTAL_FIXED_ROOF: HorizontalPhysicalFrame(self, start_read_only=start_read_only),
            TankType.VERTICAL_FIXED_ROOF: VerticalPhysicalFrame(self, start_read_only=start_read_only),
        }

        self._initial_setup()

    def _initial_setup(self) -> None:
        layout = QVBoxLayout()
        self.setLayout(layout)
        for frame in self.physical_frames.values():
            frame.setHidden(True)
            layout.addWidget(frame)

        # Default one the frame to be visible
        self.physical_frames[TankType.VERTICAL_FIXED_ROOF].setHidden(False)

    def load(self, tank: FixedRoofTank) -> None:
        # Hide all frames
        for frame in self.physical_frames.values():
            frame.setHidden(True)

        # Determine which frame to show based on the tank we need to load
        if isinstance(tank, FixedRoofTank):
            type_to_load = TankType.VERTICAL_FIXED_ROOF if tank.is_vertical else TankType.HORIZONTAL_FIXED_ROOF
        else:
            pass

        # Show the relevant frame and load the tank
        self.current_tank_type = type_to_load
        physical_frame = self.physical_frames[type_to_load]
        physical_frame.setHidden(False)
        physical_frame.load(tank)

    def unload(self) -> None:
        self.physical_frames[self.current_tank_type].unload()
