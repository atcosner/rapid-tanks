import logging
from decimal import Decimal

from src.constants.material import Material

logger = logging.getLogger(__name__)


class Mixture:
    """
    Holds a collection of materials along with the percent of each material present.
    """
    def __init__(self, name: str) -> None:
        self.name: str = name

        # List of all materials in the mixture along with their percent of the mixture
        self._materials: list[tuple[Material, Decimal]] = []

    def add_material(self, material: Material, percent: Decimal):
        self._materials.append((material, percent))

    def check(self) -> bool:
        # Sum up the percentages of materials and return if they equal 100%
        materials_sum = sum([percent.quantize(Decimal('1.0000')) for _, percent in self._materials])
        logger.info(f'Check: {materials_sum}')

        return materials_sum == Decimal(1.0)
