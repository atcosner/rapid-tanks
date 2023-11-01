import sqlite3
from pathlib import Path

from src.constants.meteorological import MeteorologicalSite, MeteorologicalMonthData
from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory


class MeteorologicalLibrary:
    def __init__(self, db_path: Path | None = None, autoload: bool = True):
        self._db_path = db_path if db_path is not None else DEV_DB_FILE_PATH

        self.sites: dict[str, MeteorologicalSite] = {}

        if not self._db_path.exists():
            raise Exception(f'DB does not exist! ({self._db_path})')

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        # Connect to the DB
        cxn = sqlite3.connect(self._db_path)
        cxn.row_factory = namedtuple_factory

        # Load the sites
        for site_row in cxn.cursor().execute('SELECT * FROM meteorological_sites'):
            site = MeteorologicalSite.from_db_row(site_row)

            # Select all detailed data for this site
            data_points = [
                MeteorologicalMonthData.from_db_row(detail_row)
                for detail_row in
                cxn.cursor().execute(f'SELECT * FROM meteorological_sites_detail WHERE site_id = {site.id}')
            ]
            for data_point in data_points:
                if data_point.month_num == 13:
                    site.annual_data = data_point
                else:
                    site.monthly_data[data_point.month_num] = data_point

            self.sites[site.name] = site

    def get_site(self, name: str) -> MeteorologicalSite | None:
        return self.sites.get(name, None)
