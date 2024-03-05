import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum, auto
from functools import lru_cache
from pint import Quantity

from src.components.mixture import Mixture
from src.constants.paint import ALL_COLORS, PaintColor, PaintCondition
from src.database.definitions.tank import FixedRoofTank
from src.util.errors import MissingData
from src.util.logging import NamedLoggerAdapter
from src.util.quantities import PI

logger = logging.getLogger(__name__)


class TankType(Enum):
    HORIZONTAL_FIXED_ROOF = auto()
    VERTICAL_FIXED_ROOF = auto()
    EXTERNAL_FLOATING_ROOF = auto()
    INTERNAL_FLOATING_ROOF = auto()


class Insulation(Enum):
    NONE = auto()
    PARTIAL = auto()  # TODO: Per AP 42 Chapter 7, this means the shell is insulated. Can it ever be only the roof?
    FULL = auto()


@dataclass
class Tank:
    """
    This is the base class for all tanks.

    All components of a tank that are similar between the both fixed and floating roof tanks should live here.
    """
    name: str
    id: int | None = None
    facility_id: int | None = None
    description: str = ''

    mixture: Mixture | None = None
    throughput: Quantity | None = None
    shell_solar_absorption: Decimal | None = None
    roof_solar_absorption: Decimal | None = None
    insulation: Insulation = Insulation.NONE  # Assume no insulation

    operational_period: tuple[date, date] | None = None

    def __post_init__(self) -> None:
        self.logger = NamedLoggerAdapter(logger, {'name': self.name})

    def set_shell_color(self, color: PaintColor, condition: PaintCondition) -> None:
        self.shell_solar_absorption = ALL_COLORS[color].get_absorption_for_condition(condition)

    def set_roof_color(self, color: PaintColor, condition: PaintCondition) -> None:
        self.roof_solar_absorption = ALL_COLORS[color].get_absorption_for_condition(condition)

    def add_mixture(self, mixture: Mixture) -> None:
        self.mixture = mixture

    def set_operational_period(self, start_date: date, end_date: date) -> None:
        self.operational_period = start_date, end_date

    def set_throughput(self, throughput: Quantity) -> None:
        self.throughput = throughput

    def get_average_solar_absorption(self) -> Decimal:
        return (self.roof_solar_absorption + self.shell_solar_absorption) / 2


@dataclass
class FixedRoofTankShim:
    """
    Shim to hold all the functions and intermediate calculations associated with a fixed roof tank.
    This is done to allow the DB definition class to not have all the complexity of the calculation equations.
    """
    tank: FixedRoofTank

    def __getattr__(self, name):
        # Allow us to pretend like we are actually the tank
        # (Priority goes to us first and then the tank)
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
                    roof_height = self.tank.roof_slope * (self.tank.shell_diameter / 2)
                roof_outage = roof_height / 3
            elif self.tank.roof_type.name == 'Dome':
                logger.debug('Calculating vapor space outage for a dome roof')
                if self.tank.roof_radius > Decimal('0.0'):
                    # TODO: Can we not use 0 as an unpopulated result?
                    tank_shell_radius = (self.tank.shell_diameter / 2)
                    roof_height = self.tank.roof_radius - (self.tank.roof_radius**2 - tank_shell_radius**2)**0.5
                    roof_outage = roof_height * (Decimal('0.5') + Decimal('0.167') * (roof_height/tank_shell_radius)**2)
                else:
                    # Use the tank shell radius instead
                    roof_outage = Decimal('0.137') * (self.tank.shell_diameter / 2)
            else:
                raise MissingData(f'Unknown roof type: {self.tank.roof_type}')

            logger.debug(f'Roof outage: {roof_outage}')

            if self.tank.average_liquid_height == Decimal('0.0'):
                # If we don't know the liquid height, assume 1/2 of tank height (Equation 1-16)
                liquid_height = (self.tank.shell_height / 2)
            else:
                liquid_height = self.tank.average_liquid_height

            vapor_space_outage = self.tank.shell_height - liquid_height + roof_outage
            logger.debug(f'Vapor space outage: {vapor_space_outage}')
            return vapor_space_outage
        else:
            # AP 42 Chapter 7 Equation 1-16 (Horizontal variant)
            # H_VO = H_E / 2
            return self.tank.shell_height / 2

    @lru_cache()
    def calculate_vapor_space_volume(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-3
        vapor_space_outage = self.calculate_vapor_space_outage()
        return (PI / 4 * self.tank.shell_diameter**2) * vapor_space_outage
