from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity


@dataclass
class OrganicLiquid:
    molecular_weight: Decimal
    vapor_constant_a: Decimal
    vapor_constant_b: Quantity
    vapor_constant_c: Quantity
    min_valid_temperature: Quantity
    max_valid_temperature: Quantity
    working_loss_product_factor: Decimal = field(default_factory=lambda: Decimal(1))
