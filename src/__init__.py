import decimal
import pint

# Restrict almost all interoperability with Python floats
# - We want to use decimals everywhere and this will make it loud if a Python float is used somewhere
decimal.getcontext().traps[decimal.FloatOperation] = True

# Use only 12 decimals of precision
decimal.getcontext().prec = 12

# Create the unit registry for everything in this package
unit_registry = pint.UnitRegistry(non_int_type=decimal.Decimal)

# Define some custom units
unit_registry.define('psia = 51.7 * mm Hg')
test = unit_registry.Quantity(decimal.Decimal('1.0'), 'mm Hg')
