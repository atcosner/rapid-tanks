import calendar
from dataclasses import dataclass
from datetime import date
from enum import Enum, auto


def get_moth_range(year: int, month: int) -> tuple[date, date]:
    return (
        date(year=year, month=month, day=1),
        date(
            year=year,
            month=month,
            day=calendar.monthrange(year, month)[1],  # (Start weekday, days in month)
        )
    )


class ReportingTimeFrame(Enum):
    ANNUAL = auto()
    MONTH = auto()
    CUSTOM = auto()


@dataclass
class ReportingPeriodChunk:
    start_date: date
    end_date: date

    def get_number_of_days(self) -> int:
        return (self.end_date - self.start_date).days


@dataclass
class ReportingPeriod:
    time_frame: ReportingTimeFrame
    year: int | None = None
    month: int | None = None
    custom_start_date: date | None = None
    custom_end_date: date | None = None

    def get_chunks(self) -> list[ReportingPeriodChunk]:
        match self.time_frame:
            case ReportingTimeFrame.ANNUAL:
                chunks = []
                for month_iter in range(1, 13):
                    start_dt, end_dt = get_moth_range(self.year, month_iter)
                    chunks.append(
                        ReportingPeriodChunk(start_date=start_dt, end_date=end_dt)
                    )
                return chunks
            case ReportingTimeFrame.MONTH:
                start_dt, end_dt = get_moth_range(self.year, self.month)
                return [ReportingPeriodChunk(start_date=start_dt, end_date=end_dt)]
            case ReportingTimeFrame.CUSTOM:
                # TODO: break this up if it spans a month boundary
                return [ReportingPeriodChunk(start_date=self.custom_start_date, end_date=self.custom_end_date)]
