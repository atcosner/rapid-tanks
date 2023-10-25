from collections import namedtuple
from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.util.quantities import to_quantity


@dataclass
class Material:
    name: str
    cas_number: str | None

    def calculate_vapor_pressure(self, average_liquid_surface_temperature: Quantity) -> Quantity:
        raise NotImplementedError()


@dataclass
class OrganicLiquid(Material):
    molecular_weight: Quantity
    vapor_constant_a: Quantity
    vapor_constant_b: Quantity
    vapor_constant_c: Quantity
    min_valid_temperature: Quantity | None
    max_valid_temperature: Quantity | None
    working_loss_product_factor: Quantity = field(default_factory=lambda: unit_registry.Quantity(Decimal(1), 'dimensionless'))

    @classmethod
    def from_namedtuple(cls, data: namedtuple):
        print(data)
        return cls(
            name=data.name,
            cas_number=data.cas_number,
            molecular_weight=unit_registry.Quantity(Decimal(data.molecular_weight), 'lb/mole'),
            vapor_constant_a=unit_registry.Quantity(Decimal(data.antoine_a), 'dimensionless'),
            vapor_constant_b=unit_registry.Quantity(Decimal(data.antoine_b), 'degC'),
            vapor_constant_c=unit_registry.Quantity(Decimal(data.antoine_c), 'degC'),
            min_valid_temperature=to_quantity(unit_registry, data.antoine_min_temp, 'degF'),
            max_valid_temperature=to_quantity(unit_registry, data.antoine_max_temp, 'degF'),
        )

    def calculate_vapor_pressure(self, average_liquid_surface_temperature: Quantity) -> Quantity:
        # AP 42 Chapter 7 Equation 1-26
        # log(P_VA) = A - (B / (T_LA + C))

        # Convert each quantity to the correct units
        a_degC = self.vapor_constant_a.magnitude
        b_degC = self.vapor_constant_b.to('degC').magnitude
        tla_degC = average_liquid_surface_temperature.to('degC').magnitude
        c_degC = self.vapor_constant_c.to('degC').magnitude

        # log(P_VA) = term1
        term1 = a_degC - (b_degC / (tla_degC + c_degC))
        p_va = unit_registry.Quantity(10**term1, 'mm Hg')

        # Result expected in psia
        return p_va.to('psia')


@dataclass
class PetroleumLiquid(Material):
    vapor_molecular_weight: Quantity
    liquid_molecular_weight: Quantity
    vapor_constant_a: Quantity
    vapor_constant_b: Quantity
    working_loss_product_factor: Decimal = field(default_factory=lambda: unit_registry.Quantity(Decimal('0.75'), 'dimensionless'))
