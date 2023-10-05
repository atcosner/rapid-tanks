from dataclasses import dataclass
from datetime import date
from decimal import Decimal

PI = Decimal('3.141592653589793')


@dataclass
class DatedQuantity:
    effective_range: tuple[date, date]  # [start, end)
    value: Decimal
