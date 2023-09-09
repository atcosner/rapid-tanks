import decimal
from sympy import symbols, init_printing, pi, srepr, preorder_traversal

init_printing()

vapor_volume, stock_vapor_density, vapor_space_expansion_factor, vented_vapor_saturation_factor = symbols('V_V W_V K_E K_S')
loss_standing = 365 * vapor_volume * stock_vapor_density * vapor_space_expansion_factor * vented_vapor_saturation_factor
print(loss_standing)

diameter, vapor_space_outage = symbols('D H_VO')
tank_vapor_space_volume = (pi / 4) * diameter**2 * vapor_space_outage
print(tank_vapor_space_volume)

test = loss_standing.subs(vapor_volume, tank_vapor_space_volume)
print(test)
print(srepr(test))
print(test.args)

for x in preorder_traversal(test):
    print(x)
