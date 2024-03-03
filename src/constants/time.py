import calendar
from dataclasses import dataclass
from datetime import date
from enum import Enum, auto


class ReportingTimeFrame(Enum):
    ANNUAL = auto()
    MONTH = auto()
    CUSTOM = auto()


@dataclass
class ReportingPeriodDetails:
    time_frame: ReportingTimeFrame
    month_id: int | None = None
    custom_start_date: date | None = None
    custom_end_date: date | None = None

    def get_reporting_days(self) -> int:
        match self.time_frame:
            case ReportingTimeFrame.ANNUAL:
                # TODO: We probably need the year number to account for leap years
                return 365
            case ReportingTimeFrame.MONTH:
                # TODO: Store year
                return calendar.monthrange(2024, self.month_id)[1]
            case ReportingTimeFrame.CUSTOM:
                return (self.custom_end_date - self.custom_start_date).days
