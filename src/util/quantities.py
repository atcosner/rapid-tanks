from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pint import UnitRegistry, Quantity

from src import unit_registry

PI = Decimal('3.141592653589793')
R = Decimal('10.731') * ((unit_registry.psi * unit_registry.ft**3) / (unit_registry.lb * unit_registry.mol * unit_registry.degR))


@dataclass
class DatedQuantity:
    effective_range: tuple[date, date]  # [start, end)
    value: Decimal


def to_quantity(registry: UnitRegistry, value: str | None, unit: str) -> Quantity | None:
    if value is None:
        return None
    else:
        return registry.Quantity(Decimal(value), unit)


def to_string(quantity: Quantity | None, unit: str, default: str = '0.0') -> str:
    if quantity is not None:
        return str(quantity.to(unit).magnitude)
    else:
        return default
