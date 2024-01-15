import logging
import sqlite3
from pathlib import Path

from src.components.facility import Facility
from src.constants.meteorological import MeteorologicalSite
from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory, get_db_connection

logger = logging.getLogger(__name__)

# TODO: I should clean this up so that there is less duplication between the select all and select one cases


class DataLibrary:
    def __init__(
            self,
            db_location: Path | sqlite3.Connection | None = None,
            preload: bool = True,
    ):
        # Establish a connection to the DB
        self.cxn = get_db_connection(db_location if db_location is not None else DEV_DB_FILE_PATH)
        self.cxn.row_factory = namedtuple_factory

        # Hold onto some constants that are expensive to load and cannot be edited by the users
        self.meteorological_sites: dict[int, MeteorologicalSite] = {}

        if preload:
            self.preload()

    def preload(self):
        # There are a lot of sites, so we should preload these
        self.meteorological_sites = {
            site.id: site for site in self.get_meteorological_site(site_id=None)
        }

    #
    # Facilities
    #

    def create_facility(self) -> Facility:
        # Create a new facility and store it in the database
        new_facility = Facility(id=-1, name='New Facility')
        new_facility.id = self.store(new_facility)
        return new_facility

    def get_facility(self, identifier: str | int | None) -> Facility | list[Facility] | None:
        if identifier is None:
            facilities = []
            for row in self.cxn.cursor().execute('SELECT * FROM facility_master'):
                facility = Facility.from_db_row(row)
                facility.meteorological_data = self.get_meteorological_site(row.meteorological_site_id)
                facilities.append(facility)

            return facilities
        else:
            # Build the where clause
            if isinstance(identifier, str):
                filter_clause = f"WHERE name = '{identifier}'"
            elif isinstance(identifier, int):
                filter_clause = f"WHERE id = {identifier}"
            else:
                raise RuntimeError(f'Unknown identifier type: {type(identifier)}')

            if row := self.cxn.cursor().execute(f'SELECT * FROM facility_master {filter_clause}').fetchone():
                facility = Facility.from_db_row(row)
                facility.meteorological_data = self.get_meteorological_site(row.meteorological_site_id)
                return facility
            else:
                logger.warning(f'Could not find a facility matching the identifier: "{identifier}"')
                return None

    def get_facility_names(self) -> list[tuple[str, int]]:
        return [
            (row.name, row.id) for row in self.cxn.cursor().execute('SELECT id, name FROM facility_master')
        ]

    def store_facility(self, facility: Facility) -> int | None:
        with self.cxn as cxn:
            cursor = self.cxn.cursor()

            # Insert or update depending on if the facility already has an id
            if facility.id:
                sql = f"""
                    UPDATE facility_master
                    SET {facility.to_db_update()}
                    WHERE id = {facility.id}
                """

                logger.info(f'Executing: "{sql}"')
                cxn.cursor().execute(sql)
                return facility.id
            else:
                sql = f'INSERT INTO facility_master VALUES {facility.to_db_values()}'

                logger.info(f'Executing: "{sql}"')
                cxn.cursor().execute(sql)
                return cursor.lastrowid

    #
    # Meteorological Sites
    #

    def get_meteorological_site(self, site_id: int | None) -> MeteorologicalSite | list[MeteorologicalSite] | None:
        # Shortcut if we have preloaded the sites
        if self.meteorological_sites:
            if site_id is None:
                return list(self.meteorological_sites.values())
            else:
                return self.meteorological_sites.get(site_id, None)

        # Fallback to the DB
        if site_id is None:
            sites = []
            for row in self.cxn.cursor().execute('SELECT * FROM meteorological_site'):
                site = MeteorologicalSite.from_db_row(row)
                site.set_monthly_data(
                    data=self.cxn.cursor().execute(
                        f'SELECT * FROM meteorological_site_detail WHERE site_id = {site.id}'
                    ).fetchall(),
                )
                sites.append(site)

            return sites
        else:
            if row := self.cxn.cursor().execute(f'SELECT * FROM meteorological_site WHERE id = {site_id}').fetchone():
                site = MeteorologicalSite.from_db_row(row)
                site.set_monthly_data(
                    data=self.cxn.cursor().execute(
                        f'SELECT * FROM meteorological_site_detail WHERE site_id = {site.id}'
                    ).fetchall(),
                )
                return site
            else:
                logger.warning(f'Could not find a site with id: "{site_id}"')
                return None
