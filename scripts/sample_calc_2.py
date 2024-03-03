import logging
from decimal import Decimal

from src.reports.calculations.fixed_roof import FixedRoofLosses
from src.components.mixture import Mixture
from src.components.facility import Facility
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

test_tank = test_site.add_fixed_roof_tank('Tank 1', vertical=False)
test_tank.set_dimensions(length=Decimal(12) * registry.foot, diameter=Decimal(6) * registry.foot)
test_tank.set_roof_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)
test_tank.set_shell_color(color=PaintColor.WHITE, condition=PaintCondition.AVERAGE)

test_tank.set_liquid_height(8 * registry.foot)
test_tank.set_throughput((8450 * registry.gallons) / registry.year)

# Load the materials we need
material_library = MaterialLibrary()
benzene = material_library.get_material('Benzene')
toluene = material_library.get_material('Toluene')
cyclohexane = material_library.get_material('Cyclohexane')

# Add the materials into a mixture
mixture = Mixture('Sample 1')
mixture.add_material(benzene, percent=Decimal('0.887'))
mixture.add_material(toluene, percent=Decimal('0.081'))
mixture.add_material(cyclohexane, percent=Decimal('0.032'))
if not mixture.check():
    raise Exception('Mixture did not equal 100%')
test_tank.add_mixture(mixture)

# Calculate site emissions
calculator = FixedRoofLosses(test_site, test_tank)
losses_per_material = calculator.calculate_total_losses()
for material_name, emissions in losses_per_material.items():
    logger.info(f'{material_name}: {emissions}')
