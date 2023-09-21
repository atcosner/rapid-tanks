import logging
from decimal import Decimal

from src.calculations.fixed_roof_losses import FixedRoofLosses
from src.components.mixture import Mixture
from src.components.site import Site
from src.components.fixed_roof_tank import VerticalRoofType
from src.constants.material import OrganicLiquid
from src.constants.meteorological import MeteorologicalData
from src.constants.paint import PaintColor, PaintCondition

from src import unit_registry as registry

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    level=logging.INFO,
)


test_site = Site('test1')

# Setup the meteorological data
weather_data = MeteorologicalData(
    average_daily_max_temp=registry.Quantity(Decimal('63.5'), 'degF'),
    average_daily_min_temp=registry.Quantity(Decimal('37.9'), 'degF'),
    solar_insolation=registry.Quantity(Decimal('1491'), 'dimensionless'),  # The unit is actually: btu/(ft^2 day)
    atmospheric_pressure=registry.Quantity(Decimal('12.08'), 'lb/inch**2'),
)
test_site.set_meteorological_data(weather_data)

test_tank = test_site.add_fixed_roof_tank('Tank 1')
test_tank.set_dimensions(height=Decimal(12) * registry.foot, diameter=Decimal(6) * registry.foot)
test_tank.set_roof_type(VerticalRoofType.CONE)
test_tank.set_roof_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)
test_tank.set_shell_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)

test_tank.set_liquid_height(8 * registry.foot)
test_tank.set_throughput((8450 * registry.gallons) / registry.year)

# Create the materials we need
benzene = OrganicLiquid(
    name='Benzene',
    cas_number='00071-43-2',
    molecular_weight=registry.Quantity(Decimal('78.11'), 'dimensionless'),
    vapor_constant_a=registry.Quantity(Decimal('6.906'), 'dimensionless'),
    vapor_constant_b=registry.Quantity(Decimal('1211.0'), 'degC'),
    vapor_constant_c=registry.Quantity(Decimal('220.79'), 'degC'),
    min_valid_temperature=registry.Quantity(Decimal('46'), 'degF'),
    max_valid_temperature=registry.Quantity(Decimal('217'), 'degF'),
)
toluene = OrganicLiquid(
    name='Toluene',
    cas_number='00108-88-3',
    molecular_weight=registry.Quantity(Decimal('92.14'), 'lb/mole'),
    vapor_constant_a=registry.Quantity(Decimal('7.017'), 'dimensionless'),
    vapor_constant_b=registry.Quantity(Decimal('1377.6'), 'degC'),
    vapor_constant_c=registry.Quantity(Decimal('222.64'), 'degC'),
    min_valid_temperature=registry.Quantity(Decimal('32'), 'degF'),
    max_valid_temperature=registry.Quantity(Decimal('122'), 'degF'),
)
cyclohexane = OrganicLiquid(
    name='Cyclohexane',
    cas_number='00110-82-7',
    molecular_weight=registry.Quantity(Decimal('84.16'), 'dimensionless'),
    vapor_constant_a=registry.Quantity(Decimal('6.845'), 'dimensionless'),
    vapor_constant_b=registry.Quantity(Decimal('1203.5'), 'degC'),
    vapor_constant_c=registry.Quantity(Decimal('222.86'), 'degC'),
    min_valid_temperature=registry.Quantity(Decimal('68'), 'degF'),
    max_valid_temperature=registry.Quantity(Decimal('179'), 'degF'),
)

# Add the materials into a mixture
mixture = Mixture('Sample 1')
mixture.add_material(benzene, percent=Decimal('0.8868'))
mixture.add_material(toluene, percent=Decimal('0.0814'))
mixture.add_material(cyclohexane, percent=Decimal('0.0318'))
if not mixture.check():
    raise Exception('Mixture did not equal 100%')
test_tank.add_mixture(mixture)

# Calculate site emissions
calculator = FixedRoofLosses(test_site, test_tank)
calculator.calculate_total_losses()
