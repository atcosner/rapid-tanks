import decimal
import pint

# Restrict almost all interoperability with Python floats
# - We want to use Decimals everywhere and this will make it loud if a Python float is used with a Decimal
decimal.getcontext().traps[decimal.FloatOperation] = True

# Use only 12 decimals of precision
decimal.getcontext().prec = 12

# Create the unit registry for everything in this package
unit_registry = pint.UnitRegistry(non_int_type=decimal.Decimal)
