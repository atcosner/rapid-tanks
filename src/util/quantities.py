from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class DatedQuantity:
    effective_range: tuple[date, date]  # [start, end)
    value: Decimal
