from decimal import Decimal
from enum import Enum, auto

from ..constants.paint import ALL_COLORS, PaintColor, PaintCondition


class Orientation(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()


class RoofType(Enum):
    DOME = auto()
    CONE = auto()


class Tank:
    """
    This tank class manages all the specifics of 1 tank at a site.

    This class handles the materials in the tank as well as dates the tanks were in service. If the client had tank
    cleanings during the year this class also needs to handle that.
    """

    def __init__(self, name: str, orientation: Orientation) -> None:
        self._orientation = orientation

        self.name: str = name
        self.shell_solar_absorption: Decimal | None = None
        self.roof_solar_absorption: Decimal | None = None

    def set_shell_color(self, color: PaintColor, condition: PaintCondition) -> None:
        paint_coefficients = ALL_COLORS[color]
        self.shell_solar_absorption = paint_coefficients.get_absorption_for_condition(condition)

    def set_roof_color(self, color: PaintColor, condition: PaintCondition) -> None:
        paint_coefficients = ALL_COLORS[color]
        self.roof_solar_absorption = paint_coefficients.get_absorption_for_condition(condition)
