from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.database.definitions.meteorological import MeteorologicalSite


@dataclass
class MeteorologicalChunk:
    average_temp: Quantity  # degF
    average_temp_min: Quantity  # degF
    average_temp_max: Quantity  # degF
    average_wind_speed: Quantity  # mph
    average_daily_insolation: Quantity  # dimensionless
    atmospheric_pressure: Quantity  # psia (Absolute PSI)

    @classmethod
    def from_site(cls, site: MeteorologicalSite, start: date, end: date):
        # Calculate the meteorological data for our range
        chunk_dates = [start + timedelta(days=i) for i in range((end - start).days + 1)]

        total_temp_min = Decimal('0.0')
        total_temp_max = Decimal('0.0')
        total_wind_speed = unit_registry.Quantity(Decimal('0.0'), 'mph')
        total_daily_insolation = unit_registry.Quantity(Decimal('0.0'), 'dimensionless')
        for chunk_date in chunk_dates:
            month_record = site.month_records[chunk_date.month]

            total_temp_min += month_record.average_temp_min.magnitude
            total_temp_max += month_record.average_temp_max.magnitude
            total_wind_speed += month_record.average_wind_speed
            total_daily_insolation += month_record.average_daily_insolation

        average_temp_min = total_temp_min / Decimal(len(chunk_dates))
        average_temp_max = total_temp_max / Decimal(len(chunk_dates))

        return cls(
            average_temp=unit_registry.Quantity((average_temp_min + average_temp_max) / 2, 'degF'),
            average_temp_min=unit_registry.Quantity(average_temp_min, 'degF'),
            average_temp_max=unit_registry.Quantity(average_temp_max, 'degF'),
            average_wind_speed=total_wind_speed / Decimal(len(chunk_dates)),
            average_daily_insolation=total_daily_insolation / Decimal(len(chunk_dates)),
            atmospheric_pressure=site.atmospheric_pressure,
        )
