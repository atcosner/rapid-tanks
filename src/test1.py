from pint import UnitRegistry

from components.site import Site
from constants.material import OrganicLiquid
from constants.paint import PaintColor, PaintCondition

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
    cas_number='',
)
