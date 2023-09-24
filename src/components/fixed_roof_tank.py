import math
from decimal import Decimal
from enum import Enum, auto
from pint import Quantity

from src import unit_registry
from src.components.tank import Tank
from src.util.errors import MissingData


class VerticalRoofType(Enum):
    DOME = auto()
    CONE = auto()


class FixedRoofTank(Tank):
    """
    This is the base class for both Vertical and Horizontal fixed roof tanks.

    Most things can be generic between horizontal and vertical tanks and should be placed here. Anything that needs to
    be specific to the orientation of the tank should be placed in the respective subclasses.
    """
    def __init__(self, name: str) -> None:
        super().__init__(name)

        # These will be set in the subclasses as they differ between horizontal and vertical
        self.diameter: Quantity | None = None
        self.height: Quantity | None = None

        self.liquid_height: Quantity | None = None

    def set_liquid_height(self, height: Quantity) -> None:
        self.liquid_height = height

    def calculate_vapor_space_outage(self) -> Quantity:
        raise NotImplementedError()

    def calculate_vapor_space_volume(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-3

        # Get the vapor space volume
        vapor_space_outage = self.calculate_vapor_space_outage()

        return (Decimal('3.14') / 4 * self.diameter**2) * vapor_space_outage


class VerticalFixedRoofTank(FixedRoofTank):
    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.roof_type: VerticalRoofType | None = None

    def set_dimensions(self, height: Quantity, diameter: Quantity) -> None:
        self.diameter = diameter
        self.height = height

    def set_roof_type(self, roof_type: VerticalRoofType) -> None:
        self.roof_type = roof_type

    def calculate_vapor_space_outage(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-16
        # H_VO = H_S − H_L+ H_RO

        # Calculate the roof outage based on the roof type
        if self.roof_type is VerticalRoofType.CONE:
            self.logger.debug('Calculating vapor space outage for a cone roof')

            roof_slope = (Decimal('0.0625') * unit_registry.foot) / unit_registry.foot
            roof_height = roof_slope * (self.diameter / 2)
            roof_outage = roof_height / 3
        elif self.roof_type is VerticalRoofType.DOME:
            # TODO
            pass
        else:
            raise MissingData(f'Unknown roof type: {self.roof_type}')

        self.logger.debug(f'Roof outage: {roof_outage}')

        # If we don't know the liquid height, assume 1/2 of tank height (Equation 1-16)
        liquid_height = self.liquid_height if self.liquid_height else (self.height / 2)

        vapor_space_outage = self.height - liquid_height + roof_outage
        self.logger.debug(f'Vapor space outage: {vapor_space_outage}')
        return vapor_space_outage


class HorizontalFixedRoofTank(FixedRoofTank):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def set_dimensions(self, length: Quantity, diameter: Quantity) -> None:
        # We need to calculate the effective height and diameter
        # Using Equation 1-14 and 1-15

        self.height = (math.pi / 4) * diameter.to('feet')
        self.diameter = math.sqrt((diameter.to('feet') * length.to('feet')) / (math.pi / 4))

    def calculate_vapor_space_outage(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-16
        # H_VO = H_E / 2
        vapor_space_outage = self.height / 2

        self.logger.debug(f'Vapor space outage: {vapor_space_outage}')
        return vapor_space_outage
