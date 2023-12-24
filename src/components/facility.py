import logging
from collections import namedtuple
from dataclasses import dataclass, field
from datetime import date

from src.components.fixed_roof_tank import HorizontalFixedRoofTank, VerticalFixedRoofTank
from src.components.tank import Tank
from src.constants.meteorological import MeteorologicalSite
from src.util.logging import NamedLoggerAdapter

logger = logging.getLogger(__name__)


@dataclass
class Facility:
    """
    The class holds all the properties/variables that are specific to the site that the tanks are located at.

    This class will need a source of meteorological data to get most of the variables a site needs to hold. The
    meteorological data can either come from the location data we ship or it can be manually input by the user into
    a custom location.
    """
    id: int
    name: str
    description: str = ''
    company: str = ''
    meteorological_data: MeteorologicalSite | None = None
    operational_period: tuple[date, date] | None = None
    tanks: dict[str, Tank] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.logger = NamedLoggerAdapter(logger, {'name': self.name})

    def to_db_row(self) -> str:
        # Handle if the meteorological data has not been set yet
        if self.meteorological_data is None:
            meteorological_id = 'NULL'
        else:
            meteorological_id = self.meteorological_data.id

        return f"""(NULL, '{self.name}', '{self.description}', '{self.company}', {meteorological_id})"""

    @classmethod
    def from_db_row(cls, row: namedtuple):
        return cls(
            id=row.id,
            name=row.name,
            description=row.description,
            company=row.company,
        )

    def set_operational_period(self, start_date: date, end_date: date) -> None:
        self.operational_period = start_date, end_date

    def set_meteorological_data(self, data: MeteorologicalSite) -> None:
        self.meteorological_data = data

    def add_fixed_roof_tank(self, name: str, vertical: bool = True) -> VerticalFixedRoofTank | HorizontalFixedRoofTank:
        self.tanks[name] = VerticalFixedRoofTank(name) if vertical else HorizontalFixedRoofTank(name)
        return self.tanks[name]
