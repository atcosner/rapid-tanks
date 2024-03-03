import sqlalchemy.types as types
from decimal import Decimal
from pint import Quantity
from typing import Any

from src import unit_registry


class PintQuantity(types.TypeDecorator):
    """Converts incoming data to the default units before sending to the database"""
    impl = types.String

    def __init__(self, default_units: str, *arg, **kw):
        super().__init__(self, *arg, **kw)
        self.impl.length = 100
        self.default_units = default_units

    def process_bind_param(self, value: Any | None, dialect) -> str | None:
        # Incoming strings are assumed to be in the correct units already
        if isinstance(value, Quantity):
            value = value.to(self.default_units)
            return str(value.magnitude)
        elif isinstance(value, str):
            return value

        return value

    def process_result_value(self, value: Any | None, dialect) -> Quantity | None:
        if value is not None:
            # Turn strings into quantities of the default units
            value = unit_registry.Quantity(Decimal(value), self.default_units)

        return value
