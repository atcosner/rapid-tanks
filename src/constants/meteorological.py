"""
This file will load the meteorological data that we save with the program. This data can be both the site 1 and 2 data
that is shipped with the program as well as custom location data that the client has input into the program.
"""

from enum import StrEnum


class Variables(StrEnum):
    AVERAGE_DAILY_MAX_TEMP = 'T~AX'
    AVERAGE_DAILY_MIN_TEMP = 'T~AN'
    SOLAR_INSOLATION = 'I'
    ATMOSPHERIC_PRESSURE = 'P~A'


class MeteorologicalLoader:
    def __init__(self) -> None:
        # self.load_bundled_data()
        # self.load_user_data()
        pass
