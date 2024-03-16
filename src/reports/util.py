from dataclasses import dataclass
from enum import Enum, auto
from pint import Quantity


class ReportOutputType(Enum):
    LOG = auto()
    PDF = auto()
    EXCEL = auto()


@dataclass
class MaterialEmission:
    material_id: int
    material_name: str
    emissions: Quantity


@dataclass
class MixtureEmission:
    mixture_id: int
    mixture_name: str
    material_emissions: list[MaterialEmission]


@dataclass
class TankEmission:
    tank_id: int
    tank_name: str
    standing_losses: list[MixtureEmission]
    working_losses: list[MixtureEmission]
