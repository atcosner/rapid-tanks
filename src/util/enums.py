from enum import IntEnum, Enum, auto, StrEnum


class MaterialType(Enum):
    PETROCHEMICAL = auto()
    PETROLEUM_LIQUID = auto()


class MixtureMakeupType(IntEnum):
    WEIGHT = 1
    VOLUME = 2
    MOLE_PERCENT = 3


class TankType(Enum):
    HORIZONTAL_FIXED_ROOF = auto()
    VERTICAL_FIXED_ROOF = auto()
    EXTERNAL_FLOATING_ROOF = auto()
    INTERNAL_FLOATING_ROOF = auto()


class InsulationType(StrEnum):
    NONE = 'None'
    PARTIAL = 'Partial'  # TODO: Per AP 42 Chapter 7, this means the shell is insulated. Can it ever be only the roof?
    FULL = 'Full'


class TankConstructionType(IntEnum):
    WELDED = 1
    RIVETED = 2
