from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from ..constants.meteorological import Variables


@dataclass
class Location:
    """
    This class is a light wrapper around some basic meteorological data that makes up a location.

    This can either be initialized from the location data that we ship with the program or can be created from custom
    set of data that is input by the user.
    """
    atmospheric_pressure: Decimal | None = None
    solar_insolation: Decimal | None = None

    def __getattr__(self, item) -> Any:
        # Check if we are trying to get one of our enum variables
        if isinstance(item, Variables):
            pass

        return getattr(super(), item)
