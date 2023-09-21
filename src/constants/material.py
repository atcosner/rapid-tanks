from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry


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
    min_valid_temperature: Quantity
    max_valid_temperature: Quantity
    working_loss_product_factor: Decimal = field(default_factory=lambda: Decimal(1))

    def calculate_vapor_pressure(self, average_liquid_surface_temperature: Quantity) -> Quantity:
        # AP 42 Chapter 7 Equation 1-26
        # log(P_VA) = A - (B / (T_LA + C))

        term1 = self.vapor_constant_a.magnitude - (self.vapor_constant_b.to('degC').magnitude / (average_liquid_surface_temperature.to('degC').magnitude + self.vapor_constant_c.to('degC').magnitude))
        return unit_registry.Quantity(10**term1, 'mm Hg').to('psia')


@dataclass
class PetroleumLiquid(Material):
    vapor_molecular_weight: Quantity
    liquid_molecular_weight: Quantity
    vapor_constant_a: Quantity
    vapor_constant_b: Quantity
    working_loss_product_factor: Decimal = field(default_factory=lambda: Decimal(0.75))
