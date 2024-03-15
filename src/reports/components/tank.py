import logging
from dataclasses import dataclass
from decimal import Decimal
from functools import lru_cache
from pint import Quantity

from src import unit_registry
from src.database.definitions.tank import FixedRoofTank
from src.util.errors import MissingData
from src.util.quantities import PI

logger = logging.getLogger(__name__)


@dataclass
class FixedRoofTankShim:
    """
    Shim to hold all the functions and intermediate calculations associated with a fixed roof tank.
    This is done to allow the DB definition class to not have all the complexity of the calculation equations.
    """
    tank: FixedRoofTank

    # Separate these to allow for adjustments for horizontal tanks
    shell_height: Decimal | None = None
    shell_diameter: Decimal | None = None

    def __post_init__(self) -> None:
        if self.tank.is_vertical:
            # No adjustments for vertical tanks
            self.shell_height = self.tank.shell_height
            self.shell_diameter = self.tank.shell_diameter
        else:
            # Equation 1-14 - Effective Diameter
            effective_diameter = ((self.tank.shell_height.magnitude * self.tank.shell_diameter.magnitude) / (PI / 4)).sqrt()
            self.shell_diameter = effective_diameter * unit_registry.ft

            # Equation 1-15 - Effective Height
            self.shell_height = (PI / 4) * self.tank.shell_diameter

    def __getattr__(self, name):
        # Allow us to pretend like we are actually the tank
        # (Priority goes to the wrapper first and then the tank itself)
        if name in self.__dict__:
            return self[name]
        elif hasattr(self.tank, name):
            return getattr(self.tank, name)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __hash__(self) -> int:
        # Use the tank's id as our hash
        return self.tank.id

    @lru_cache()
    def calculate_vapor_space_outage(self) -> Quantity:
        if self.tank.is_vertical:
            # AP 42 Chapter 7 Equation 1-16 (Vertical variant)
            # H_VO = H_S − H_L + H_RO

            # Calculate the roof outage based on the roof type
            if self.tank.roof_type.name == 'Cone':
                logger.debug('Calculating vapor space outage for a cone roof')
                if self.tank.roof_height > Decimal('0.0'):
                    # TODO: Can we not use 0 as an unpopulated result?
                    roof_height = self.tank.roof_height
                else:
                    roof_height = self.tank.roof_slope * (self.shell_diameter / 2)
                roof_outage = roof_height / 3
            elif self.tank.roof_type.name == 'Dome':
                logger.debug('Calculating vapor space outage for a dome roof')
                if self.tank.roof_radius > Decimal('0.0'):
                    # TODO: Can we not use 0 as an unpopulated result?
                    tank_shell_radius = (self.shell_diameter / 2)
                    roof_height = self.tank.roof_radius - (self.tank.roof_radius**2 - tank_shell_radius**2)**0.5
                    roof_outage = roof_height * (Decimal('0.5') + Decimal('0.167') * (roof_height/tank_shell_radius)**2)
                else:
                    # Use the tank shell radius instead
                    roof_outage = Decimal('0.137') * (self.shell_diameter / 2)
            else:
                raise MissingData(f'Unknown roof type: {self.tank.roof_type}')

            logger.debug(f'Roof outage: {roof_outage}')

            if self.tank.average_liquid_height == Decimal('0.0'):
                # If we don't know the liquid height, assume 1/2 of tank height (Equation 1-16)
                liquid_height = (self.shell_height / 2)
            else:
                liquid_height = self.tank.average_liquid_height

            vapor_space_outage = self.shell_height - liquid_height + roof_outage
            logger.debug(f'Vapor space outage: {vapor_space_outage}')
            return vapor_space_outage
        else:
            # AP 42 Chapter 7 Equation 1-16 (Horizontal variant)
            # H_VO = H_E / 2
            return self.shell_height / 2

    @lru_cache()
    def calculate_vapor_space_volume(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-3
        vapor_space_outage = self.calculate_vapor_space_outage()
        return (PI / 4 * self.shell_diameter**2) * vapor_space_outage
