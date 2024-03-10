import logging
from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.database.definitions.material import Petrochemical
from src.database.definitions.mixture import PetrochemicalMixture
from src.util.enums import MixtureMakeupType

logger = logging.getLogger(__name__)


@dataclass
class MaterialShim:
    material: Petrochemical
    makeup_value: Decimal

    # Calculated values
    moles: Decimal | None = None
    mole_fraction: Decimal | None = None
    vapor_weight_fraction: Decimal | None = None
    partial_pressure: Quantity | None = None
    vapor_molecular_weight: Quantity | None = None
    vapor_pressure: dict[Quantity, Quantity] = field(default_factory=dict)

    def calculate_vapor_pressure(self, average_liquid_surface_temperature: Quantity) -> Quantity:
        # AP 42 Chapter 7 Equation 1-26
        # log(P_VA) = A - (B / (T_LA + C))

        # Convert each quantity to the correct units
        a__degc = self.material.vapor_constant_a.magnitude
        b__degc = self.material.vapor_constant_b.to('degC').magnitude
        tla__degc = average_liquid_surface_temperature.to('degC').magnitude
        c__degc = self.material.vapor_constant_c.to('degC').magnitude

        # log(P_VA) = term1
        term1 = a__degc - (b__degc / (tla__degc + c__degc))
        p_va = unit_registry.Quantity(10**term1, 'mm Hg').to('psi')

        self.vapor_pressure[average_liquid_surface_temperature] = p_va
        return self.vapor_pressure[average_liquid_surface_temperature]


@dataclass
class MixtureShim:
    name: str
    makeup_type: MixtureMakeupType
    components: list[MaterialShim]

    # Calculated values
    total_moles: Decimal | None = None
    vapor_pressure: dict[Quantity, Quantity] = field(default_factory=dict)

    @classmethod
    def from_mixture(cls, mixture: PetrochemicalMixture):
        materials = []
        for component in mixture.components:
            materials.append(
                MaterialShim(
                    material=component.material,
                    makeup_value=Decimal(component.value),
                )
            )

        obj = cls(
            name=mixture.name,
            makeup_type=MixtureMakeupType(mixture.makeup_type_id),
            components=materials,
        )
        obj.calculate_mole_fractions()
        return obj

    def calculate_mole_fractions(self) -> None:
        match self.makeup_type:
            case MixtureMakeupType.WEIGHT:
                for component in self.components:
                    makeup__g = component.makeup_value * unit_registry.lb
                    component.moles = makeup__g.to('g') / component.material.molecular_weight
                self.total_moles = sum([component.moles for component in self.components])
                for component in self.components:
                    component.mole_fraction = component.moles / self.total_moles
                    logger.debug(f'{component.material.name} | Mole Fraction: {component.mole_fraction}')

            case MixtureMakeupType.VOLUME:
                # TODO: We are going to need densities for this makeup type
                pass

            case MixtureMakeupType.MOLE_PERCENT:
                for component in self.components:
                    component.mole_fraction = component.makeup_value

    def calculate_vapor_pressure(self, temperature: Quantity) -> Quantity:
        # Calculate the partial pressure of each part of the mixture
        mixture_vapor_pressure = Decimal('0') * unit_registry.psi
        for component in self.components:
            # Calculate the pure vapor pressure of the part
            pure_vapor_pressure = component.calculate_vapor_pressure(temperature)
            logger.debug(f'{component.material.name} | Vapor Pressure: {pure_vapor_pressure} @ {temperature}')

            # Calculate the partial pressure
            component.partial_pressure = component.mole_fraction * pure_vapor_pressure
            mixture_vapor_pressure += component.partial_pressure

        self.vapor_pressure[temperature] = mixture_vapor_pressure
        return mixture_vapor_pressure

    def calculate_vapor_molecular_weight(self, temperature: Quantity) -> Quantity:
        # Check if we already have the mixture vapor pressure
        if (mixture_vapor_pressure := self.vapor_pressure.get(temperature)) is None:
            mixture_vapor_pressure = self.calculate_vapor_pressure(temperature)

        # Calculate percents of partial pressures over the mixture vapor pressure
        total_vapor_molecular_weight = Decimal('0') * unit_registry.g / unit_registry.mole
        for component in self.components:
            # Vapor percent
            vapor_percent = component.partial_pressure / mixture_vapor_pressure
            logger.debug(f'{component.material.name} | Vapor Percent: {vapor_percent} @ {temperature}')

            component.vapor_molecular_weight = vapor_percent * component.material.molecular_weight
            logger.debug(f'{component.material.name} | Partial vapor molecular weight: {component.vapor_molecular_weight}')

            total_vapor_molecular_weight += component.vapor_molecular_weight

        # Now that we have the total vapor molecular weight, calculate the weight fraction
        for component in self.components:
            component.vapor_weight_fraction = component.vapor_molecular_weight / total_vapor_molecular_weight

        return total_vapor_molecular_weight
