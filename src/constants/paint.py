from decimal import Decimal
from typing import NamedTuple


class PaintCoefficients(NamedTuple):
    color_name: str
    new: Decimal
    average: Decimal
    aged: Decimal


ALL_COLORS = [
    PaintCoefficients('White',                  Decimal(0.17), Decimal(0.25), Decimal(0.34)),
    PaintCoefficients('Aluminum - Specular',    Decimal(0.39), Decimal(0.44), Decimal(0.49)),
    PaintCoefficients('Aluminum - Diffuse',     Decimal(0.60), Decimal(0.64), Decimal(0.68)),
    PaintCoefficients('Beige/Cream',            Decimal(0.35), Decimal(0.42), Decimal(0.49)),
    PaintCoefficients('Black',                  Decimal(0.97), Decimal(0.97), Decimal(0.97)),
    PaintCoefficients('Brown',                  Decimal(0.58), Decimal(0.62), Decimal(0.67)),
    PaintCoefficients('Light Gray',             Decimal(0.54), Decimal(0.58), Decimal(0.63)),
    PaintCoefficients('Medium Gray',            Decimal(0.68), Decimal(0.71), Decimal(0.74)),
    PaintCoefficients('Dark Green',             Decimal(0.89), Decimal(0.90), Decimal(0.91)),
    PaintCoefficients('Red',                    Decimal(0.89), Decimal(0.90), Decimal(0.91)),
    PaintCoefficients('Rust',                   Decimal(0.38), Decimal(0.44), Decimal(0.50)),
    PaintCoefficients('Tan',                    Decimal(0.43), Decimal(0.49), Decimal(0.55)),
    PaintCoefficients('Unpainted',              Decimal(0.10), Decimal(0.12), Decimal(0.15)),
]
