import logging
from decimal import Decimal

from src.calculations.fixed_roof_losses import FixedRoofLosses
from src.components.mixture import Mixture
from src.components.facility import Facility
from src.components.fixed_roof_tank import VerticalRoofType
from src.constants.paint import PaintColor, PaintCondition
from src.data.material_library import MaterialLibrary
from src.data.meteorological_library import MeteorologicalLibrary
from src.util.logging import configure_root_logger

from src import unit_registry as registry

configure_root_logger()

logger = logging.getLogger(__name__)


test_site = Facility(0, 'test1')

# Load the meteorological data
meteorological_library = MeteorologicalLibrary()
site_weather_data = meteorological_library.get_sites_by_name('Denver')[0]
test_site.set_meteorological_data(site_weather_data)

test_tank = test_site.add_fixed_roof_tank('Tank 1')
test_tank.set_dimensions(height=Decimal(12) * registry.foot, diameter=Decimal(6) * registry.foot)
test_tank.set_roof_type(VerticalRoofType.CONE)
test_tank.set_roof_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)
test_tank.set_shell_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)

test_tank.set_liquid_height(8 * registry.foot)
test_tank.set_throughput((8450 * registry.gallons) / registry.year)

# Load the materials we need
material_library = MaterialLibrary()
no2_fuel_oil = material_library.get_material('No. 2 Fuel Oil')
no6_fuel_oil = material_library.get_material('No. 6 Fuel Oil')

# Add the materials into a mixture
mixture = Mixture('Sample 1')
mixture.add_material(no2_fuel_oil, percent=Decimal('0.5'))
mixture.add_material(no6_fuel_oil, percent=Decimal('0.5'))
if not mixture.check():
    raise Exception('Mixture did not equal 100%')
test_tank.add_mixture(mixture)

# Calculate site emissions
calculator = FixedRoofLosses(test_site, test_tank)
losses_per_material = calculator.calculate_total_losses()
for material_name, emissions in losses_per_material.items():
    logger.info(f'{material_name}: {emissions}')
