import logging
from collections import defaultdict
from decimal import Decimal

from ..util import TankEmission

logger = logging.getLogger(__name__)


class LogOutput:
    @staticmethod
    def report(tank_emissions: list[TankEmission]) -> None:
        emissions_by_tank = defaultdict(Decimal)
        emissions_by_mixture = defaultdict(Decimal)
        emissions_by_material = defaultdict(Decimal)

        for tank_emissions in tank_emissions:
            standing = (tank_emissions.standing_losses, tank_emissions.standing_losses.material_emissions)
            working = (tank_emissions.working_losses, tank_emissions.working_losses.material_emissions)
            for mixture, materials in [standing, working]:
                for material in materials:
                    material_key = (material.material_id, material.material_name)
                    emissions_by_material[material_key] += material.emissions

                    mixture_key = (mixture.mixture_id, mixture.mixture_name)
                    emissions_by_mixture[mixture_key] += material.emissions

                    tank_key = (tank_emissions.tank_id, tank_emissions.tank_id)
                    emissions_by_tank[tank_key] += material.emissions

        # Log the results
        for (_, name), emissions in emissions_by_tank.items():
            logger.info(f'Tank {name}: {emissions}')

        for (_, name), emissions in emissions_by_mixture.items():
            logger.info(f'Mixture {name}: {emissions}')

        for (_, name), emissions in emissions_by_material.items():
            logger.info(f'Material {name}: {emissions}')
