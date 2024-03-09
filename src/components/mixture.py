import logging
from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.constants.material import Material, Petrochemical
from src.database.definitions.material import Petrochemical
from src.util.enums import MixtureMakeupType

logger = logging.getLogger(__name__)


@dataclass
class MixtureComponent:
    material: Material
    weight_fraction: Decimal

    # These can be calculated once we have all materials added to the mixture
    mole_fraction: Decimal | None = None
    weight_fraction: Decimal | None = None
    partial_pressure: Quantity | None = None
    vapor_molecular_weight: Quantity | None = None
    vapor_pressure: dict = field(default_factory=dict)

    def get_liquid_molecular_weight(self) -> Quantity:
        if isinstance(self.material, Petrochemical):
            return self.material.molecular_weight
        else:
            return self.material.liquid_molecular_weight

    def get_vapor_molecular_weight(self) -> Quantity:
        if isinstance(self.material, Petrochemical):
            return self.material.molecular_weight
        else:
            return self.material.vapor_molecular_weight


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
            part_mixture_weight = 100 * part.weight_fraction * unit_registry.lb
            temp_moles = part_mixture_weight / part.get_liquid_molecular_weight()
            total_moles += temp_moles

        # Calculate the partial pressure of each part of the mixture
        mixture_vapor_pressure = Decimal('0') * unit_registry.psia
        for part in self.parts:
            # Calculate mole fraction
            moles = (100 * part.weight_fraction * unit_registry.lb) / part.get_liquid_molecular_weight()
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

            part.vapor_molecular_weight = vapor_percent * part.get_vapor_molecular_weight()
            logger.debug(f'{part.material.name} | Partial vapor molecular weight: {part.vapor_molecular_weight}')

            total_vapor_molecular_weight += part.vapor_molecular_weight

        # Now that we have the total vapor molecular weight, calculate the weight fraction
        for part in self.parts:
            part.weight_fraction = part.vapor_molecular_weight / total_vapor_molecular_weight

        return total_vapor_molecular_weight

    def add_material(self, material: Material, percent: Decimal):
        self.parts.append(MixtureComponent(material, percent))

    def check(self) -> bool:
        # Sum up the percentages of materials and return if they equal 100%

        # Restruct to 4 decimal places of precision
        materials_sum = sum([part.weight_fraction.quantize(Decimal('1.0000')) for part in self.parts])
        logger.info(f'Total material percent: {materials_sum}')

        return materials_sum == Decimal(1)


@dataclass
class MaterialShim:
    material: Petrochemical
    makeup_value: Decimal


@dataclass
class MixtureShim:
    """
    Shim to hold all the functions and intermediate calculations associated with a mixture and associated materials.
    This is done to allow the DB definition class to not have all the complexity of the calculation equations.
    """
    name: str
    makeup_type: MixtureMakeupType
    materials: list[MaterialShim]
