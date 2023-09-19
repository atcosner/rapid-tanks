import logging

from src.components.site import Site
from src.components.fixed_roof_tank import FixedRoofTank

logger = logging.getLogger(__name__)


class FixedRoofLosses:
    def __init__(self, site: Site) -> None:
        self.site = site

    def _calculate_standing_losses(self, tank: FixedRoofTank):
        logger.info(f'Calculating standing losses for "{tank.name}" at "{self.site.name}"')

        # AP 42 Chapter 7 Equation 1-2
        # L~S = 365 * V~V * W~V * K~E * K~S

        # Get the vapor space outage from the tank
        vapor_space_outage = tank.calculate_vapor_space_outage()

    def calculate_total_losses(self, tank: FixedRoofTank):
        logger.info(f'Calculating total losses for "{tank.name}" at "{self.site.name}"')

        # Start with standing losses
        self._calculate_standing_losses(tank)
