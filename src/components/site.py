import logging
from datetime import date
from pint import UnitRegistry

from src.components.fixed_roof_tank import HorizontalFixedRoofTank, VerticalFixedRoofTank
from src.components.tank import Tank
from src.constants.meteorological import MeteorologicalData
from src.util.logging import NamedLoggerAdapter

logger = logging.getLogger(__name__)


class Site:
    """
    The class holds all the properties/variables that are specific to the site that the tanks are located at.

    This class will need a source of meteorological data to get most of the variables a site needs to hold. The
    meteorological data can either come from the location data we ship or it can be manually input by the user into
    a custom location.
    """

    def __init__(self, name: str, unit_registry: UnitRegistry) -> None:
        self.name: str = name
        self.logger = NamedLoggerAdapter(logger, {'name': self.name})

        self._unit_registry: UnitRegistry | None = unit_registry

        self._meteorological_data: MeteorologicalData | None = None
        self._operational_period: tuple[date, date] | None = None
        self._tanks: dict[str, Tank] = {}

    def set_operational_period(self, start_date: date, end_date: date) -> None:
        self._operational_period = start_date, end_date

    def set_meteorological_data(self, data: MeteorologicalData) -> None:
        self._meteorological_data = data

    def add_fixed_roof_tank(self, name: str, vertical: bool = True) -> VerticalFixedRoofTank | HorizontalFixedRoofTank:
        self._tanks[name] = VerticalFixedRoofTank(name) if vertical else HorizontalFixedRoofTank(name)
        self._tanks[name].set_unit_registry(self._unit_registry)
        return self._tanks[name]
