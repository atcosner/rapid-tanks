from collections import namedtuple
from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.util.quantities import to_quantity


@dataclass
class Material:
    name: str

    def calculate_vapor_pressure(self, average_liquid_surface_temperature: Quantity) -> Quantity:
        raise NotImplementedError()


@dataclass
class Petrochemical(Material):
    cas_number: str | None
    molecular_weight: Quantity
    vapor_constant_a: Quantity
    vapor_constant_b: Quantity
    vapor_constant_c: Quantity
    min_valid_temperature: Quantity | None
    max_valid_temperature: Quantity | None
    normal_boiling_point: Quantity | None
    working_loss_product_factor: Quantity = field(default_factory=lambda: unit_registry.Quantity(Decimal(1), 'dimensionless'))

    @classmethod
    def from_db_row(cls, row: namedtuple):
        return cls(
            name=row.name,
            cas_number=row.cas_number,
            molecular_weight=unit_registry.Quantity(Decimal(row.molecular_weight), 'lb/mole'),
            vapor_constant_a=unit_registry.Quantity(Decimal(row.antoine_a), 'dimensionless'),
            vapor_constant_b=unit_registry.Quantity(Decimal(row.antoine_b), 'degC'),
            vapor_constant_c=unit_registry.Quantity(Decimal(row.antoine_c), 'degC'),
            min_valid_temperature=to_quantity(unit_registry, row.antoine_min_temp, 'degF'),
            max_valid_temperature=to_quantity(unit_registry, row.antoine_max_temp, 'degF'),
            normal_boiling_point=to_quantity(unit_registry, row.normal_boiling_point, 'degF'),
        )

    def to_db_row(self) -> str:
        # TODO: Add the rest of the DB columns to this class

        # Convert the internal quantities to the right units
        molecular_weight_str = self.molecular_weight.to('lb/mole').magnitude
        vapor_constant_a_str = self.vapor_constant_a.to('dimensionless').magnitude
        vapor_constant_b_str = self.vapor_constant_b.to('degC').magnitude
        vapor_constant_c_str = self.vapor_constant_c.to('degC').magnitude
        min_valid_temperature_str = self.min_valid_temperature.to('degF').magnitude
        max_valid_temperature_str = self.max_valid_temperature.to('degF').magnitude
        normal_boiling_point_str = self.normal_boiling_point.to('degF').magnitude

        return f"""(NULL, '{self.name}', '{self.cas_number}', '{molecular_weight_str}', NULL, NULL,
                   '{vapor_constant_a_str}', '{vapor_constant_b_str}', '{vapor_constant_c_str}',
                   '{min_valid_temperature_str}', '{max_valid_temperature_str}', {normal_boiling_point_str})"""

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
    vapor_molecular_weight: Quantity | None
    liquid_molecular_weight: Quantity | None
    vapor_constant_a: Quantity | None
    vapor_constant_b: Quantity | None
    working_loss_product_factor: Decimal = field(default_factory=lambda: unit_registry.Quantity(Decimal('0.75'), 'dimensionless'))

    @classmethod
    def from_db_row(cls, row: namedtuple):
        return cls(
            name=row.name,
            vapor_molecular_weight=to_quantity(unit_registry, row.vapor_molecular_weight, 'lb/mole'),
            liquid_molecular_weight=to_quantity(unit_registry, row.liquid_molecular_weight, 'lb/mole'),
            vapor_constant_a=to_quantity(unit_registry, row.vapor_pressure_eq_a, 'dimensionless'),
            vapor_constant_b=to_quantity(unit_registry, row.vapor_pressure_eq_b, 'degR'),
        )

    def to_db_row(self) -> str:
        # TODO: Add the rest of the DB columns to this class

        # Convert the internal quantities to the right units
        vapor_molecular_weight_str = self.vapor_molecular_weight.to('lb/mole').magnitude
        liquid_molecular_weight_str = self.liquid_molecular_weight.to('lb/mole').magnitude
        vapor_constant_a_str = self.vapor_constant_a.to('dimensionless').magnitude
        vapor_constant_b_str = self.vapor_constant_b.to('degR').magnitude

        return f"""(NULL, '{self.name}', '{vapor_molecular_weight_str}', '{liquid_molecular_weight_str}',
                   NULL, NULL, '{vapor_constant_a_str}', '{vapor_constant_b_str}', NULL)"""

    def calculate_vapor_pressure(self, average_liquid_surface_temperature: Quantity) -> Quantity:
        # This needs to be calculated multiple ways based on what information we have

        if self.vapor_constant_a is not None and self.vapor_constant_b is not None:
            # AP 42 Chapter 7 Equation 1-25
            # P_VA = exp[A - (B / T_LA)]

            # Convert each quantity to the correct units
            b_degR = self.vapor_constant_b.to('degR').magnitude
            tla_degR = average_liquid_surface_temperature.to('degR').magnitude

            # Calculate the inner portion
            temp1 = self.vapor_constant_a.magnitude - (b_degR / tla_degR)

            return unit_registry.Quantity(temp1.exp(), 'psia')
        else:
            # TODO: Implement other ways to calculate this
            raise RuntimeError()
