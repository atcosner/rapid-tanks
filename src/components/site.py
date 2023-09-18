import logging
from datetime import date

from .fixed_roof_tank import FixedRoofTank, VerticalFixedRoofTank, HorizontalFixedRoofTank
from src.constants.meteorological import MeteorologicalData
from src.util.errors import MissingData
from src.util.logging import NamedLoggerAdapter

logger = logging.getLogger(__name__)


class Site:
    """
    The class holds all the properties/variables that are specific to the site that the tanks are located at.

    This class will need a source of meteorological data to get most of the variables a site needs to hold. The
    meteorological data can either come from the location data we ship or it can be manually input by the user into
    a custom location.
    """

    def __init__(self, name: str) -> None:
        self.site_name: str = name
        self.logger = NamedLoggerAdapter(logger, {'name': self.site_name})

        self._meteorological_data: MeteorologicalData | None = None
        self._operational_period: tuple[date, date] | None = None
        self._tanks: dict[str, HorizontalFixedRoofTank | VerticalFixedRoofTank] = {}

    def set_operational_period(self, start_date: date, end_date: date) -> None:
        self._operational_period = start_date, end_date

    def set_meteorological_data(self, data: MeteorologicalData) -> None:
        self._meteorological_data = data

    def add_horizontal_tank(self, name: str) -> HorizontalFixedRoofTank:
        self._tanks[name] = HorizontalFixedRoofTank(name)
        return self._tanks[name]

    def add_vertical_tank(self, name: str) -> VerticalFixedRoofTank:
        self._tanks[name] = VerticalFixedRoofTank(name)
        return self._tanks[name]

    def calculate_emissions(self):
        # Ensure we have what we need
        if self._meteorological_data is None:
            self.logger.error('No meteorological data')
            raise MissingData('No meteorological data')

        # Assume the whole year if no operational range is specified
        if self._operational_period is None:
            operational_days = 365  # TODO: Leap year?
        else:
            operational_days = (self._operational_period[1] - self._operational_period[0]).days

        # Calculate the emissions tank by tank
        for name, tank in self._tanks.items():
            self.logger.info(f'Calculating emissions for tank: {name}')
