import calendar
from dataclasses import dataclass
from datetime import date
from enum import Enum, auto
from pint import Quantity

from .meteorological import MeteorologicalChunk
from .mixture import MixtureShim


class ReportingTimeFrame(Enum):
    ANNUAL = auto()
    MONTH = auto()
    CUSTOM = auto()


def get_moth_range(year: int, month: int) -> tuple[date, date]:
    return (
        date(year=year, month=month, day=1),
        date(
            year=year,
            month=month,
            day=calendar.monthrange(year, month)[1],  # (Start weekday, days in month)
        )
    )


@dataclass
class ReportingChunk:
    start_date: date
    end_date: date
    site: MeteorologicalChunk
    throughput: Quantity
    mixture: MixtureShim

    def total_days(self) -> int:
        return (self.end_date - self.start_date).days


@dataclass
class ReportingPeriod:
    time_frame: ReportingTimeFrame
    year: int | None = None
    month: int | None = None
    custom_start_date: date | None = None
    custom_end_date: date | None = None

    def get_date_range(self) -> tuple[date, date]:
        match self.time_frame:
            case ReportingTimeFrame.ANNUAL:
                return date(year=self.year, month=1, day=1), date(year=self.year, month=12, day=31)
            case ReportingTimeFrame.MONTH:
                return get_moth_range(self.year, self.month)
            case ReportingTimeFrame.CUSTOM:
                return self.custom_start_date, self.custom_end_date
