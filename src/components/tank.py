import logging
from datetime import date
from decimal import Decimal
from pint import Quantity, UnitRegistry

from src.components.mixture import Mixture
from src.constants.paint import ALL_COLORS, PaintColor, PaintCondition
from src.util.errors import MissingData
from src.util.logging import NamedLoggerAdapter

logger = logging.getLogger(__name__)


class Tank:
    """
    This is the base class for all tanks.

    All components of a tank that are similar between the roof types should live in here.
    """
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.logger = NamedLoggerAdapter(logger, {'name': self.name})

        self.mixture: Mixture | None = None
        self.throughput: Quantity | None = None
        self.shell_solar_absorption: Decimal | None = None
        self.roof_solar_absorption: Decimal | None = None
        self.operational_period: tuple[date, date] | None = None

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

    def check_setup(self) -> None:
        """Check if we have the required components to calculate emissions"""
        if self.mixture is None:
            raise MissingData(f'Tank "{self.name}" did not have a mixture set!')
