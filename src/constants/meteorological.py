"""
This file will load the meteorological data that we save with the program. This data can be both the site 1 and 2 data
that is shipped with the program as well as custom location data that the client has input into the program.
"""

from collections import namedtuple
from dataclasses import dataclass, field
from decimal import Decimal
from pint import Quantity

from src import unit_registry


@dataclass
class MeteorologicalMonthData:
    month_num: int
    average_daily_min_temp: Quantity
    average_daily_max_temp: Quantity
    average_wind_speed: Quantity
    average_solar_insolation: Quantity

    @classmethod
    def from_db_row(cls, row: namedtuple):
        return cls(
            month_num=row.month_id,
            average_daily_min_temp=unit_registry.Quantity(Decimal(row.average_temp_min), 'degF'),
            average_daily_max_temp=unit_registry.Quantity(Decimal(row.average_temp_max), 'degF'),
            average_wind_speed=unit_registry.Quantity(Decimal(row.average_wind_speed), 'mi/hr'),
            average_solar_insolation=unit_registry.Quantity(Decimal(row.average_daily_insolation), 'dimensionless'),  # The unit is actually: btu/(ft^2 day)
        )


@dataclass
class MeteorologicalSite:
    id: int
    name: str
    gps_coordinates: tuple[str, str]
    atmospheric_pressure: Quantity
    monthly_data: dict[int, MeteorologicalMonthData] = field(default_factory=dict)
    annual_data: MeteorologicalMonthData | None = None

    @classmethod
    def from_db_row(cls, row: namedtuple):
        return cls(
            id=row.id,
            name=row.name,
            gps_coordinates=(row.gps_latitude, row.gps_longitude),
            atmospheric_pressure=unit_registry.Quantity(Decimal(row.atmospheric_pressure), 'psia'),
        )
