from dataclasses import dataclass
from enum import Enum, auto


class ReportOutputType(Enum):
    PDF = auto()
    EXCEL = auto()


@dataclass
class MaterialEmission:
    material_id: int
    emission_value: str
    emission_unit: str


@dataclass
class TankEmission:
    material_emissions: list[MaterialEmission]
