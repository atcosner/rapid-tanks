import logging
import sqlite3
from pathlib import Path

from src.components.facility import Facility
from src.constants.meteorological import MeteorologicalSite
from src.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory, get_db_connection

from .meteorological_library import MeteorologicalLibrary

logger = logging.getLogger(__name__)


class FacilityLibrary:
    def __init__(
            self,
            db_location: Path | sqlite3.Connection | None = None,
            autoload: bool = True,
    ):
        # Establish a connection to the DB
        self.cxn = get_db_connection(db_location if db_location is not None else DEV_DB_FILE_PATH)
        self.cxn.row_factory = namedtuple_factory

        self.meteorological_library = MeteorologicalLibrary(self.cxn, autoload)

        self.facilities: dict[str, Facility] = {}

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        cursor = self.cxn.cursor()

        # Load the facilities
        for row in cursor.execute('SELECT * FROM facility_master'):
            facility = Facility.from_db_row(row)
            facility.meteorological_data = self.meteorological_library.get_site_by_id(row.meteorological_site_id)
            self.facilities[facility.name] = facility

    def reload(self) -> None:
        # Remove all existing entries
        self.facilities.clear()

        # Load from the DB
        self.load_from_db()

        # Reload any libraries we have
        self.meteorological_library.reload()

    def get_facility_by_name(self, name: str) -> Facility | None:
        return self.facilities.get(name, None)

    def get_facility_by_id(self, facility_id: int) -> Facility | None:
        for facility in self.facilities.values():
            if facility.id == facility_id:
                return facility
        return None

    def store(self, facility: Facility) -> int | None:
        with self.cxn:
            cursor = self.cxn.cursor()

            # Insert or update depending on if the facility already has an id
            if facility.id:
                sql = f"""
                    UPDATE facility
                    SET {facility.to_db_update()}
                    WHERE id = {facility.id}
                """

                logger.info(f'Executing: "{sql}"')
                cursor.execute(sql)
                return facility.id
            else:
                sql = f'INSERT INTO facility VALUES {facility.to_db_values()}'

                logger.info(f'Executing: "{sql}"')
                cursor.execute(sql)
                return cursor.lastrowid

    def create(self) -> Facility:
        # Create a new facility and store it in the database
        new_facility = Facility(id=-1, name=f'New Facility ({len(self.facilities)})')
        new_facility.id = self.store(new_facility)
        return new_facility

    def update_meteorological_site(self, facility_id: int, site: MeteorologicalSite) -> None:
        with self.cxn as cxn:
            sql = f"""
                UPDATE facility
                SET meteorological_site_id = {site.id}
                WHERE id = {facility_id}
            """

            logger.info(f'Executing: "{sql}"')
            cxn.execute(sql)

        # Update our local facility
        if facility := self.get_facility_by_id(facility_id):
            facility.meteorological_data = site
        else:
            # TODO: How did we get here?
            raise RuntimeError(f'Could not find facility with id: {facility_id}')
