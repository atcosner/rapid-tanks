from datetime import date

from .fixed_roof_tank import FixedRoofTank, VerticalFixedRoofTank, HorizontalFixedRoofTank


class Site:
    """
    The class holds all the properties/variables that are specific to the site that the tanks are located at.

    This class will need a source of meteorological data to get most of the variables a site needs to hold. The
    meteorological data can either come from the location data we ship or it can be manually input by the user into
    a custom location.
    """

    def __init__(self, name: str) -> None:
        self.site_name: str = name

        self._operational_period: tuple[date, date] | None = None
        self._tanks: dict[str, HorizontalFixedRoofTank | VerticalFixedRoofTank] = {}

    def set_operational_period(self, start_date: date, end_date: date) -> None:
        self._operational_period = start_date,end_date

    def add_horizontal_tank(self, name: str) -> HorizontalFixedRoofTank:
        self._tanks[name] = HorizontalFixedRoofTank(name)
        return self._tanks[name]

    def add_vertical_tank(self, name: str) -> VerticalFixedRoofTank:
        self._tanks[name] = VerticalFixedRoofTank(name)
        return self._tanks[name]
