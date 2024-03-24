from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.database.definitions.material import Petrochemical, PetroleumLiquid
from src.util.enums import MaterialType


@dataclass
class MaterialShim:
    material_type: MaterialType
    material: Petrochemical | PetroleumLiquid
    makeup_value: Decimal

    # Calculated values
    moles: Decimal | None = None
    mole_fraction: Decimal | None = None
    vapor_weight_fraction: Decimal | None = None
    partial_pressure: Quantity | None = None
    vapor_molecular_weight: Quantity | None = None
    vapor_pressure: dict[Quantity, Quantity] = field(default_factory=dict)

    def calculate_vapor_pressure(self, average_liquid_surface_temperature: Quantity) -> Quantity:
        if self.material_type == MaterialType.PETROLEUM_LIQUID:
            # AP 42 Chapter 7 Equation 1-25
            # P_VA = exp[A - (B / T_LA)]

            a = self.material.vapor_constant_a.magnitude
            b__degr = self.material.vapor_constant_b.to('degR').magnitude
            tla__degr = average_liquid_surface_temperature.to('degR').magnitude

            p_va = (a - (b__degr / tla__degr)).exp() * unit_registry.psi

        else:
            # AP 42 Chapter 7 Equation 1-26
            # log(P_VA) = A - (B / (T_LA + C))

            # Convert each quantity to the correct units
            a = self.material.vapor_constant_a.magnitude
            b__degc = self.material.vapor_constant_b.to('degC').magnitude
            tla__degc = average_liquid_surface_temperature.to('degC').magnitude
            c__degc = self.material.vapor_constant_c.to('degC').magnitude

            # log(P_VA) = term1
            term1 = a - (b__degc / (tla__degc + c__degc))
            p_va = unit_registry.Quantity(10**term1, 'mm Hg').to('psi')

        self.vapor_pressure[average_liquid_surface_temperature] = p_va
        return self.vapor_pressure[average_liquid_surface_temperature]
