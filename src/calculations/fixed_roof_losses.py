import logging
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.components.fixed_roof_tank import FixedRoofTank
from src.components.site import Site
from src.components.tank import Insulation
from src.util.errors import CalculationError

logger = logging.getLogger(__name__)


class FixedRoofLosses:
    def __init__(self, site: Site, tank: FixedRoofTank) -> None:
        self.site = site
        self.tank = tank

        # Store intermediate calculations here
        self.vapor_space_outage: Quantity | None = None
        self.average_ambient_temperature: Quantity | None = None
        self.liquid_bulk_temperature: Quantity | None = None
        self.average_daily_liquid_surface_temperature: Quantity | None = None

    def _calculate_average_daily_ambient_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-30
        weather_data = self.site.meteorological_data

        # Use the meteorological data from the site
        # TODO: This needs to be adjusted for the time period we are calculating over
        average_daily_temp = (weather_data.average_daily_max_temp.to('degR')
                              + weather_data.average_daily_min_temp.to('degR')
                              ) / 2
        return average_daily_temp.magnitude * unit_registry.degR

    def _calculate_liquid_bulk_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-31
        bulk_temp = self.average_ambient_temperature.to('degR').magnitude \
                    + (Decimal('0.003')
                       * self.tank.shell_solar_absorption
                       * self.site.meteorological_data.solar_insolation)

        return bulk_temp.magnitude * unit_registry.degR

    def _calculate_average_daily_liquid_surface_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-27, 1-28, and 1-29

        # This is based on which type of insulation the tank has
        if self.tank.insulation is Insulation.NONE:
            # Do not make assumptions and use equation 1-28, just use equation 1-27
            term1 = self.average_ambient_temperature.to('degR').magnitude \
                    * (Decimal('0.5') - (Decimal('0.8') / (Decimal('4.4') * (self.tank.height / self.tank.diameter) + Decimal('3.8'))))

            term2 = self.liquid_bulk_temperature.to('degR').magnitude \
                    * (Decimal('0.5') + (Decimal('0.8') / (Decimal('4.4') * (self.tank.height / self.tank.diameter) + Decimal('3.8'))))

            term3 = (
                        (Decimal('0.021') * self.tank.roof_solar_absorption * self.site.meteorological_data.solar_insolation)
                        + (Decimal('0.013') * (self.tank.height / self.tank.diameter) * self.tank.shell_solar_absorption * self.site.meteorological_data.solar_insolation)
                    ) / (
                        Decimal('4.4') * (self.tank.height / self.tank.diameter) + Decimal('3.8')
                    )

            return (term1.magnitude + term2.magnitude + term3.magnitude) * unit_registry.degR

        elif self.tank.insulation is Insulation.PARTIAL:
            # Equation 1-28
            return (Decimal('0.4') * self.average_ambient_temperature.to('degR')) \
                   + (Decimal('0.06') * self.liquid_bulk_temperature.to('degR')) \
                   + (Decimal('0.005')
                      * self.tank.get_average_solar_absorption()
                      * self.site.meteorological_data.solar_insolation)

        elif self.tank.insulation is Insulation.FULL:
            # Equation 1-29
            return self.liquid_bulk_temperature.to('degR')

        else:
            # What?
            raise CalculationError(f'Unknown insulation: {self.tank.insulation}')

    def _calculate_standing_losses(self) -> Quantity:
        logger.info(f'Calculating standing losses for "{self.tank.name}" at "{self.site.name}"')

        # AP 42 Chapter 7 Equation 1-2
        # L~S = 365 * V~V * W~V * K~E * K~S

        # Determine the days we are calculating losses over
        days = 365  # TODO: Actually do this

        # Get the vapor space outage from the tank
        self.vapor_space_outage = self.tank.calculate_vapor_space_outage()
        logger.info(f'Vapor space outage: {self.vapor_space_outage}')

        # Calculate the average daily ambient temperature
        self.average_ambient_temperature = self._calculate_average_daily_ambient_temperature()
        logger.info(f'Average daily ambient temperature: {self.average_ambient_temperature}')

        # Calculate the liquid bulk temperature
        self.liquid_bulk_temperature = self._calculate_liquid_bulk_temperature()
        logger.info(f'Liquid bulk temperature: {self.liquid_bulk_temperature}')

        # Calculate the average daily liquid surface temperature
        self.average_daily_liquid_surface_temperature = self._calculate_average_daily_liquid_surface_temperature()
        logger.info(f'Average daily liquid surface temperature: {self.average_daily_liquid_surface_temperature}')

        # Calculate vapor pressure for each material
        for material, _ in self.tank.mixture.materials:
            vapor_pressure = material.calculate_vapor_pressure(self.average_daily_liquid_surface_temperature)
            logger.info(f'{material.name} | Vapor Pressure: {vapor_pressure}')

    def calculate_total_losses(self):
        logger.info(f'Calculating total losses for "{self.tank.name}" at "{self.site.name}"')

        # Start with standing losses
        self._calculate_standing_losses()
