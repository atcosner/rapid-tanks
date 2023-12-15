from collections import namedtuple
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from pint import Quantity

from src import unit_registry
from src.components.tank import Tank
from src.util.errors import MissingData
from src.util.quantities import PI


class VerticalRoofType(Enum):
    DOME = auto()
    CONE = auto()


@dataclass
class FixedRoofTank(Tank):
    """
    This is the base class for both Vertical and Horizontal fixed roof tanks.

    Most things can be generic between horizontal and vertical tanks and should be placed here. Anything that needs to
    be specific to the orientation of the tank should be placed in the respective subclasses.
    """

    # These will be set in the subclasses as they differ between horizontal and vertical
    diameter: Quantity | None = None
    height: Quantity | None = None
    liquid_height: Quantity | None = None

    def set_liquid_height(self, height: Quantity) -> None:
        self.liquid_height = height

    def calculate_vapor_space_outage(self) -> Quantity:
        raise NotImplementedError()

    def calculate_vapor_space_volume(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-3

        # Get the vapor space volume
        vapor_space_outage = self.calculate_vapor_space_outage()

        return (PI / 4 * self.diameter**2) * vapor_space_outage


@dataclass
class VerticalFixedRoofTank(FixedRoofTank):
    roof_type: VerticalRoofType | None = None
    roof_height: Quantity | None = None
    roof_slope: Quantity | None = None
    roof_radius: Quantity | None = None

    def to_db_row(self) -> str:
        # Convert the internal quantities to the right units
        shell_height_str = self.height.to('ft').magnitude
        shell_diameter_str = self.diameter.to('ft').magnitude
        roof_height_str = self.roof_height.to('ft').magnitude
        roof_slope_str = self.roof_slope.to('ft/ft').magnitude
        roof_radius_str = self.roof_radius.to('ft').magnitude

        # TODO: Handle all values
        return f"""(
            NULL,
            '{self.identifier}',
            '{self.description}',
            1,
            TRUE,
            '{shell_height_str}',
            '{shell_diameter_str}',
            1,
            1,
            1,
            1,
            1,
            '{roof_height_str}',
            '{roof_slope_str}',
            '{roof_radius_str}',
            '-0.3',
            '0.3',
            '0',
            '0',
            '0',
            '0',
            '0',
            FALSE
        )"""

    @classmethod
    def from_db_row(cls, row: namedtuple):
        # TODO: Handle all values
        return cls(
            identifier=row.name,
            description=row.description,
            height=unit_registry.Quantity(Decimal(row.shell_height), 'ft'),
            diameter=unit_registry.Quantity(Decimal(row.shell_diameter), 'ft'),
            roof_height=unit_registry.Quantity(Decimal(row.roof_height), 'ft'),
            roof_slope=unit_registry.Quantity(Decimal(row.roof_slope), 'ft/ft'),
            roof_radius=unit_registry.Quantity(Decimal(row.roof_radius), 'ft'),
        )

    def calculate_vapor_space_outage(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-16
        # H_VO = H_S − H_L + H_RO

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

        diameter_ft = diameter.to('feet')
        length_ft = length.to('feet')

        self.height = (PI / 4) * diameter_ft
        self.logger.debug(f'Effective Height: {self.height}')

        effective_diameter = ((diameter_ft.magnitude * length_ft.magnitude) / (PI / 4)).sqrt()
        self.diameter = effective_diameter * unit_registry.feet
        self.logger.debug(f'Effective Diameter: {self.diameter}')

    def calculate_vapor_space_outage(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-16
        # H_VO = H_E / 2
        vapor_space_outage = self.height / 2

        self.logger.debug(f'Vapor space outage: {vapor_space_outage}')
        return vapor_space_outage
