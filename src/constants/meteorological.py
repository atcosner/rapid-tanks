from dataclasses import dataclass
from pint import Quantity

from src.constants.time import ReportingPeriodDetails, ReportingTimeFrame
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

    def get_average_daily_ambient_temperature(self, reporting_period: ReportingPeriodDetails) -> Quantity:
        # AP 42 Chapter 7 Equation 1-30

        match reporting_period.time_frame:
            case ReportingTimeFrame.ANNUAL:
                avg_max_temp__degr = self.get_annual_data().average_temp_max.to('degR')
                avg_min_temp__degr = self.get_annual_data().average_temp_min.to('degR')
            case ReportingTimeFrame.MONTH:
                avg_max_temp__degr = self.site.month_records[reporting_period.month_id].average_temp_max.to('degR')
                avg_min_temp__degr = self.site.month_records[reporting_period.month_id].average_temp_min.to('degR')
            case ReportingTimeFrame.CUSTOM:
                # TODO: Implement this
                pass

        return (avg_max_temp__degr + avg_min_temp__degr) / 2
