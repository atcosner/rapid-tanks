from decimal import Decimal
from pint import UnitRegistry

unit_registry = UnitRegistry(non_int_type=Decimal)
