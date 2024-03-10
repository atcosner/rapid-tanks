from dataclasses import dataclass
from enum import Enum, auto
from pint import Quantity


class ReportOutputType(Enum):
    LOG = auto()  # TODO: Remove once we can generate PDF reports
    PDF = auto()
    EXCEL = auto()


@dataclass
class MaterialEmission:
    material_id: int
    material_name: str
    emissions: Quantity


@dataclass
class TankEmission:
    material_emissions: list[MaterialEmission]
