import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum, auto
from pint import Quantity

from src.components.mixture import Mixture
from src.constants.paint import ALL_COLORS, PaintColor, PaintCondition
from src.util.logging import NamedLoggerAdapter

logger = logging.getLogger(__name__)


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
    id: int = -1
    description: str = ''

    mixture: Mixture | None = None
    throughput: Quantity | None = None
    shell_solar_absorption: Decimal | None = None
    roof_solar_absorption: Decimal | None = None
    insulation: Insulation = Insulation.NONE  # Assume no insulation

    operational_period: tuple[date, date] | None = None

    def __post_init__(self) -> None:
        self.logger = NamedLoggerAdapter(logger, {'name': self.identifier})

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
