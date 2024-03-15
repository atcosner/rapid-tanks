import logging
from collections import defaultdict
from decimal import Decimal

from ..util import TankEmission

logger = logging.getLogger(__name__)


class LogOutput:
    @staticmethod
    def report(tank_emissions: list[TankEmission]) -> None:
        emissions_by_tank = defaultdict(Decimal)
        emissions_by_material = defaultdict(Decimal)

        for tank_emissions in tank_emissions:
            for material_emissions in tank_emissions.material_emissions:
                material_key = (material_emissions.material_id, material_emissions.material_name)
                emissions_by_material[material_key] += material_emissions.emissions

                tank_key = (tank_emissions.tank_id, tank_emissions.tank_id)
                emissions_by_tank[tank_key] += material_emissions.emissions

        # Log the results
        for (_, name), emissions in emissions_by_tank.items():
            logger.info(f'Tank {name}: {emissions}')

        for (_, name), emissions in emissions_by_material.items():
            logger.info(f'Material {name}: {emissions}')
