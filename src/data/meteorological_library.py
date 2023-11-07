import sqlite3
from pathlib import Path

from src.constants.meteorological import MeteorologicalSite, MeteorologicalMonthData
from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory, get_db_connection


class MeteorologicalLibrary:
    def __init__(self, db_location: Path | sqlite3.Connection | None = None, autoload: bool = True):
        # Establish a connection to the DB
        self.cxn = get_db_connection(db_location if db_location is not None else DEV_DB_FILE_PATH)
        self.cxn.row_factory = namedtuple_factory

        self.sites: dict[str, MeteorologicalSite] = {}

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        # Load the sites
        for location_row in self.cxn.cursor().execute('SELECT * FROM meteorological_location'):
            site = MeteorologicalSite.from_db_row(location_row)

            # Select all detailed data for this site
            data_points = [
                MeteorologicalMonthData.from_db_row(detail_row)
                for detail_row in
                self.cxn.cursor().execute(f'SELECT * FROM meteorological_location_detail WHERE site_id = {site.id}')
            ]
            for data_point in data_points:
                if data_point.month_num == 13:
                    site.annual_data = data_point
                else:
                    site.monthly_data[data_point.month_num] = data_point

            self.sites[site.name] = site

    def reload(self) -> None:
        # Remove all existing entries
        self.sites.clear()

        # Load from the DB
        self.load_from_db()

    def get_site(self, name: str) -> MeteorologicalSite | None:
        return self.sites.get(name, None)
