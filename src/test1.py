import logging
from decimal import Decimal
from pint import UnitRegistry, Quantity

from components.mixture import Mixture
from components.site import Site
from constants.material import OrganicLiquid
from constants.paint import PaintColor, PaintCondition

logging.basicConfig(level=logging.INFO)

ureg = UnitRegistry()

test_site = Site('test1')
test_tank = test_site.add_vertical_tank('Tank 1')

# Setup dimensions on the tank
test_tank.set_dimensions(height=12 * ureg.foot, diameter=6 * ureg.foot)

# Set the colors
test_tank.set_roof_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)
test_tank.set_roof_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)

# Create the materials we need
benzene = OrganicLiquid(
    name='Benzene',
    cas_number='00071-43-2',
    molecular_weight=Quantity(78.11, 'dimensionless'),
    vapor_constant_a=Quantity(76.906, 'dimensionless'),
    vapor_constant_b=Quantity(1211.0, 'degC'),
    vapor_constant_c=Quantity(220.79, 'degC'),
    min_valid_temperature=Quantity(46, 'degF'),
    max_valid_temperature=Quantity(217, 'degF'),
)
toluene = OrganicLiquid(
    name='Toluene',
    cas_number='00108-88-3',
    molecular_weight=Quantity(92.14, 'dimensionless'),
    vapor_constant_a=Quantity(7.017, 'dimensionless'),
    vapor_constant_b=Quantity(1377.6, 'degC'),
    vapor_constant_c=Quantity(222.64, 'degC'),
    min_valid_temperature=Quantity(32, 'degF'),
    max_valid_temperature=Quantity(122, 'degF'),
)
cyclohexane = OrganicLiquid(
    name='Cyclohexane',
    cas_number='00110-82-7',
    molecular_weight=Quantity(84.16, 'dimensionless'),
    vapor_constant_a=Quantity(6.845, 'dimensionless'),
    vapor_constant_b=Quantity(1203.5, 'degC'),
    vapor_constant_c=Quantity(222.86, 'degC'),
    min_valid_temperature=Quantity(68, 'degF'),
    max_valid_temperature=Quantity(179, 'degF'),
)

# Add the materials into a mixture
mixture = Mixture('Sample 1')
mixture.add_material(benzene, percent=Decimal(0.8868))
mixture.add_material(toluene, percent=Decimal(0.0814))
mixture.add_material(cyclohexane, percent=Decimal(0.0318))
if not mixture.check():
    raise Exception('Mixture did not equal 100%')

test_tank.add_mixture(mixture)

