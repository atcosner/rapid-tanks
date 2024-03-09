from dataclasses import dataclass
from pint import Quantity

from src.constants.time import ReportingPeriodChunk, ReportingTimeFrame
from src.database.definitions.meteorological import MeteorologicalSite, MeteorologicalMonthRecord


@dataclass
class MeteorologicalSiteShim:
    """
    Shim to hold all the functions and intermediate calculations associated with a meteorological site.
    This is done to allow the DB definition class to not have all the complexity of the calculation equations.
    """
    site: MeteorologicalSite

    def get_annual_data(self) -> MeteorologicalMonthRecord:
        return self.site.month_records[13]

    def get_average_daily_ambient_temperature(self, reporting_chunk: ReportingPeriodChunk) -> Quantity:
        # AP 42 Chapter 7 Equation 1-30

        # TODO: Implement this to actually use the reporting chunk
        avg_max_temp__degr = self.get_annual_data().average_temp_max.to('degR')
        avg_min_temp__degr = self.get_annual_data().average_temp_min.to('degR')

        return (avg_max_temp__degr + avg_min_temp__degr) / 2
