import logging
from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.database.definitions.mixture import Mixture
from src.reports.components.material import MaterialShim
from src.util.enums import MixtureMakeupType, MaterialType

logger = logging.getLogger(__name__)


@dataclass
class MixtureShim:
    name: str
    db_id: int
    makeup_type: MixtureMakeupType
    components: list[MaterialShim]

    # Calculated values
    total_moles: Decimal | None = None
    vapor_pressure: dict[Quantity, Quantity] = field(default_factory=dict)

    @classmethod
    def from_mixture(cls, mixture: Mixture):
        materials = []
        for component in mixture.components:
            if component.petrochemical is not None:
                shim = MaterialShim(
                    material_type=MaterialType.PETROCHEMICAL,
                    material=component.petrochemical,
                    makeup_value=Decimal(component.value),
                )
            else:
                shim = MaterialShim(
                    material_type=MaterialType.PETROLEUM_LIQUID,
                    material=component.petroleum_liquid,
                    makeup_value=Decimal(component.value),
                )

            materials.append(shim)

        obj = cls(
            name=mixture.name,
            db_id=mixture.id,
            makeup_type=MixtureMakeupType(mixture.makeup_type_id),
            components=materials,
        )
        obj.calculate_mole_fractions()
        return obj

    def calculate_mole_fractions(self) -> None:
        match self.makeup_type:
            case MixtureMakeupType.WEIGHT:
                for component in self.components:
                    makeup__lb = component.makeup_value * unit_registry.lb
                    component.moles = makeup__lb / component.material.molecular_weight
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
        total_vapor_molecular_weight = Decimal('0') * unit_registry.lb / unit_registry.mole
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
