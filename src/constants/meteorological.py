"""
This file will load the meteorological data that we save with the program. This data can be both the site 1 and 2 data
that is shipped with the program as well as custom location data that the client has input into the program.
"""

from dataclasses import dataclass
from pint import Quantity


@dataclass
class MeteorologicalData:
    average_daily_max_temp: Quantity
    average_daily_min_temp: Quantity
    solar_insolation: Quantity
    atmospheric_pressure: Quantity


class MeteorologicalLoader:
    def __init__(self) -> None:
        # self.load_bundled_data()
        # self.load_user_data()
        pass
