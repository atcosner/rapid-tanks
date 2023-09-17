from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, StrEnum, auto


class PaintColor(StrEnum):
    WHITE = 'White'
    ALUMINUM_SPECULAR = 'Aluminum - Specular'
    ALUMINUM_DIFFUSE = 'Aluminum - Diffuse'
    BEIGE = 'Beige/Cream'
    BLACK = 'Black'
    BROWN = 'Brown'
    LIGHT_GRAY = 'Light Gray'
    MEDIUM_GRAY = 'Medium Gray'
    DARK_GREEN = 'Dark Green'
    RED = 'Red'
    RUST = 'Rust'
    TAN = 'Tan'
    UNPAINTED = 'Unpainted'
    UNKNOWN = 'Unknown'


class PaintCondition(Enum):
    NEW = auto()
    AVERAGE = auto()
    AGED = auto()


@dataclass
class SolarAbsorptanceCoefficients:
    new: Decimal
    average: Decimal
    aged: Decimal

    def get_absorption_for_condition(self, condition: PaintCondition) -> Decimal:
        match condition:
            case PaintCondition.NEW:
                return self.new
            case PaintCondition.AVERAGE:
                return self.average
            case PaintCondition.AGED:
                return self.aged


ALL_COLORS = {
    PaintColor.WHITE:               SolarAbsorptanceCoefficients(Decimal(0.17), Decimal(0.25), Decimal(0.34)),
    PaintColor.ALUMINUM_SPECULAR:   SolarAbsorptanceCoefficients(Decimal(0.39), Decimal(0.44), Decimal(0.49)),
    PaintColor.ALUMINUM_DIFFUSE:    SolarAbsorptanceCoefficients(Decimal(0.60), Decimal(0.64), Decimal(0.68)),
    PaintColor.BEIGE:               SolarAbsorptanceCoefficients(Decimal(0.35), Decimal(0.42), Decimal(0.49)),
    PaintColor.BLACK:               SolarAbsorptanceCoefficients(Decimal(0.97), Decimal(0.97), Decimal(0.97)),
    PaintColor.BROWN:               SolarAbsorptanceCoefficients(Decimal(0.58), Decimal(0.62), Decimal(0.67)),
    PaintColor.LIGHT_GRAY:          SolarAbsorptanceCoefficients(Decimal(0.54), Decimal(0.58), Decimal(0.63)),
    PaintColor.MEDIUM_GRAY:         SolarAbsorptanceCoefficients(Decimal(0.68), Decimal(0.71), Decimal(0.74)),
    PaintColor.DARK_GREEN:          SolarAbsorptanceCoefficients(Decimal(0.89), Decimal(0.90), Decimal(0.91)),
    PaintColor.RED:                 SolarAbsorptanceCoefficients(Decimal(0.89), Decimal(0.90), Decimal(0.91)),
    PaintColor.RUST:                SolarAbsorptanceCoefficients(Decimal(0.38), Decimal(0.44), Decimal(0.50)),
    PaintColor.TAN:                 SolarAbsorptanceCoefficients(Decimal(0.43), Decimal(0.49), Decimal(0.55)),
    PaintColor.UNPAINTED:           SolarAbsorptanceCoefficients(Decimal(0.10), Decimal(0.12), Decimal(0.15)),
    PaintColor.UNKNOWN:             SolarAbsorptanceCoefficients(Decimal(0.17), Decimal(0.25), Decimal(0.34)),  # White
}
