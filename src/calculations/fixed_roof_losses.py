import logging
from decimal import Decimal
from pint import Quantity

from src.components.site import Site
from src.components.fixed_roof_tank import FixedRoofTank

logger = logging.getLogger(__name__)


class FixedRoofLosses:
    def __init__(self, site: Site) -> None:
        self.site = site

    def _calculate_average_daily_ambient_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-30
        weather_data = self.site.meteorological_data

        # Use the meteorological data from the site
        # TODO: This needs to be adjusted for the time period we are calculating over
        average_daily_temp = (weather_data.average_daily_max_temp.to('degR') + weather_data.average_daily_min_temp.to('degR')) / 2
        return average_daily_temp.to('degR')

    def _calculate_liquid_bulk_temperature(self, tank: FixedRoofTank, average_ambient_temp: Quantity) -> Quantity:
        # AP 42 Chapter 7 Equation 1-31
        bulk_temp = average_ambient_temp.to('degR') + (Decimal('0.003') * tank.shell_solar_absorption * self.site.meteorological_data.solar_insolation)
        return bulk_temp.to('degR')

    def _calculate_standing_losses(self, tank: FixedRoofTank):
        logger.info(f'Calculating standing losses for "{tank.name}" at "{self.site.name}"')

        # AP 42 Chapter 7 Equation 1-2
        # L~S = 365 * V~V * W~V * K~E * K~S

        # Determine the days we are calculating losses over
        days = 365  # TODO: Actually do this

        # Get the vapor space outage from the tank
        vapor_space_outage = tank.calculate_vapor_space_outage()

        # Calculate the average daily ambient temperature
        average_ambient_temperature = self._calculate_average_daily_ambient_temperature()
        logger.info(f'Average daily ambient temperature: {average_ambient_temperature}')

        # Calculate the liquid bulk temperature
        liquid_bulk_temp = self._calculate_liquid_bulk_temperature(tank, average_ambient_temperature)
        logger.info(f'Liquid bulk temperature: {liquid_bulk_temp}')

    def calculate_total_losses(self, tank: FixedRoofTank):
        logger.info(f'Calculating total losses for "{tank.name}" at "{self.site.name}"')

        # Start with standing losses
        self._calculate_standing_losses(tank)
