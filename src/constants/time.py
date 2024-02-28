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
