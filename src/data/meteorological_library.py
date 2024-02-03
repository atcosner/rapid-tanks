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

        self.sites: dict[id, MeteorologicalSite] = {}

        if autoload:
            self.load_from_db()

    # Allow iterating through the class as if it was the site dict
    def __iter__(self):
        yield from self.sites.items()

    def load_from_db(self) -> None:
        # Load the sites
        for location_row in self.cxn.cursor().execute('SELECT * FROM meteorological_site'):
            site = MeteorologicalSite.from_db_row(location_row)

            # Select all detailed data for this site
            data_points = [
                MeteorologicalMonthData.from_db_row(detail_row)
                for detail_row in
                self.cxn.cursor().execute(f'SELECT * FROM meteorological_month_record WHERE site_id = {site.id}')
            ]
            for data_point in data_points:
                if data_point.month_num == 13:
                    site.annual_data = data_point
                else:
                    site.monthly_data[data_point.month_num] = data_point

            self.sites[site.id] = site

    def reload(self) -> None:
        # Remove all existing entries
        self.sites.clear()

        # Load from the DB
        self.load_from_db()

    def get_site_by_id(self, site_id: int) -> MeteorologicalSite | None:
        return self.sites.get(site_id, None)

    def get_sites_by_name(self, site_name: str) -> list[MeteorologicalSite] | None:
        # Site could have the same name so we return all matches
        # TODO: Casing?
        matches = [site for site in self.sites.values() if site.name == site_name]
        return matches if matches else None

    def get_sites_by_state(self, state_name: str) -> list[MeteorologicalSite]:
        return [site for site in self.sites.values() if site.state.lower() == state_name.lower()]
