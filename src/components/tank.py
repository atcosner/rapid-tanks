from enum import Enum, auto


class TankOrientation(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class TankRoof(Enum):
    DOME = auto()
    CONE = auto()


class Tank:
    """
    This tank class manages all the specifics of 1 tank at a site.

    This class handles the materials in the tank as well as dates the tanks were in service. If the client had tank
    cleanings during the year this class also needs to handle that.
    """

    def __init__(self, orientation: TankOrientation) -> None:
        self._orientation = orientation

        self._shell_paint: | None = None
        self._roof_paint: | None = None

    def set_shell_color(self, paint_):
