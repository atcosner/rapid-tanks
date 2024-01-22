from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pint import UnitRegistry, Quantity

PI = Decimal('3.141592653589793')


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
