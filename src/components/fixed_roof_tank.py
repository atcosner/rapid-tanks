import math
from decimal import Decimal
from enum import Enum, auto
from pint import Quantity

from src.components.mixture import Mixture
from src.constants.paint import ALL_COLORS, PaintColor, PaintCondition


class RoofType(Enum):
    DOME = auto()
    CONE = auto()


class FixedRoofTank:
    """
    This is the base class for both Vertical and Horizontal fixed roof tanks.

    Most things can be generic between horizontal and vertical tanks and should be placed here. Anything that needs to
    be specific to the orientation of the tank should be placed in the respective subclasses.
    """
    def __init__(self, name: str) -> None:
        self.name: str = name

        # These will be set in the subclasses as they differ between horizontal and vertical
        self.diameter: Quantity | None = None
        self.height: Quantity | None = None

        self.mixture: Mixture | None = None

        self.shell_solar_absorption: Decimal | None = None
        self.roof_solar_absorption: Decimal | None = None

    def set_shell_color(self, color: PaintColor, condition: PaintCondition) -> None:
        self.shell_solar_absorption = ALL_COLORS[color].get_absorption_for_condition(condition)

    def set_roof_color(self, color: PaintColor, condition: PaintCondition) -> None:
        self.roof_solar_absorption = ALL_COLORS[color].get_absorption_for_condition(condition)

    def add_mixture(self, mixture: Mixture) -> None:
        self.mixture = mixture


class VerticalFixedRoofTank(FixedRoofTank):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def set_dimensions(self, height: Quantity, diameter: Quantity) -> None:
        self.diameter = diameter
        self.height = height


class HorizontalFixedRoofTank(FixedRoofTank):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def set_dimensions(self, length: Quantity, diameter: Quantity) -> None:
        # We need to calculate the effective height and diameter
        # Using Equation 1-14 and 1-15

        self.height = (math.pi / 4) * diameter.to('feet')
        self.diameter = math.sqrt((diameter.to('feet') * length.to('feet')) / (math.pi / 4))
