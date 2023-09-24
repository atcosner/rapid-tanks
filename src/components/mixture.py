import logging
from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.constants.material import Material

logger = logging.getLogger(__name__)


@dataclass
class MixtureComponent:
    material: Material
    weight_fraction: Decimal

    # These can be calculated once we have all materials added to the mixture
    mole_fraction: Decimal | None = None
    partial_pressure: Quantity | None = None
    vapor_pressure: dict = field(default_factory=dict)


class Mixture:
    """
    Holds a collection of materials along with the percent of each material present.
    """
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.parts: list[MixtureComponent] = []

        # These can be calculated once we have all materials added to the mixture
        self.vapor_pressure: dict[Quantity, Quantity] = {}

    def calculate_vapor_pressure(self, temperature: Quantity) -> Quantity:
        # Determine the total moles in a predefined weight
        total_moles = Decimal('0') * unit_registry.mole
        for part in self.parts:
            # Use a standard mixture weight of 100 lbs
            total_moles += (100 * part.weight_fraction * unit_registry.lb) / part.material.molecular_weight

        # Calculate the partial pressure of each part of the mixture
        mixture_vapor_pressure = Decimal('0') * unit_registry.psia
        for part in self.parts:
            # Calculate mole fraction
            moles = (100 * part.weight_fraction * unit_registry.lb) / part.material.molecular_weight
            part.mole_fraction = moles / total_moles
            logger.debug(f'{part.material.name} | Mole Fraction: {part.mole_fraction}')

            # Calculate the pure vapor pressure of the part
            part.vapor_pressure[temperature] = part.material.calculate_vapor_pressure(temperature)
            logger.debug(f'{part.material.name} | Vapor Pressure: {part.vapor_pressure[temperature]} @ {temperature}')

            # Calculate the partial pressure
            part.partial_pressure = part.mole_fraction * part.vapor_pressure[temperature]
            mixture_vapor_pressure += part.partial_pressure

        self.vapor_pressure[temperature] = mixture_vapor_pressure
        return mixture_vapor_pressure

    def calculate_vapor_molecular_weight(self, temperature: Quantity):
        # Check if we already have the mixture vapor pressure
        if (mixture_vapor_pressure := self.vapor_pressure.get(temperature)) is None:
            mixture_vapor_pressure = self.calculate_vapor_pressure(temperature)

        # Calculate percents of partial pressures over the mixture vapor pressure
        total_vapor_molecular_weight = Decimal('0') * unit_registry.lb / unit_registry.mole
        for part in self.parts:
            # Vapor percent
            vapor_percent = part.partial_pressure / mixture_vapor_pressure
            logger.debug(f'{part.material.name} | Vapor Percent: {vapor_percent} @ {temperature}')

            part_molecular_weight = vapor_percent * part.material.molecular_weight
            logger.debug(f'{part.material.name} | Partial vapor molecular weight: {part_molecular_weight}')

            total_vapor_molecular_weight += part_molecular_weight

        return total_vapor_molecular_weight

    def add_material(self, material: Material, percent: Decimal):
        self.parts.append(MixtureComponent(material, percent))

    def check(self) -> bool:
        # Sum up the percentages of materials and return if they equal 100%

        # Restruct to 4 decimal places of precision
        materials_sum = sum([part.weight_fraction.quantize(Decimal('1.0000')) for part in self.parts])
        logger.info(f'Total material percent: {materials_sum}')

        return materials_sum == Decimal(1)
