import sqlite3
from pathlib import Path

from src.components.facility import Facility
from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory, get_db_connection


class FacilityLibrary:
    def __init__(self, db_location: Path | sqlite3.Connection | None = None, autoload: bool = True):
        # Establish a connection to the DB
        self.cxn = get_db_connection(db_location if db_location is not None else DEV_DB_FILE_PATH)
        self.cxn.row_factory = namedtuple_factory

        self.facilities: dict[str, Facility] = {}

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        cursor = self.cxn.cursor()

        # Load the facilities
        for row in cursor.execute('SELECT * FROM facility_master'):
            facility = Facility.from_db_row(row)
            self.facilities[facility.name] = facility

    def reload(self) -> None:
        # Remove all existing entries
        self.facilities.clear()

        # Load from the DB
        self.load_from_db()

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
            facility_row = facility.to_db_row()
            cursor.execute(f'INSERT INTO facility_master VALUES {facility_row}')
            return cursor.lastrowid
