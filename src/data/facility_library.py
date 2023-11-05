import sqlite3
from pathlib import Path

from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory, get_db_connection


class MeteorologicalLibrary:
    def __init__(self, db_location: Path | sqlite3.Connection | None = None, autoload: bool = True):
        # Establish a connection to the DB
        self.cxn = get_db_connection(db_location if db_location is not None else DEV_DB_FILE_PATH)
        self.cxn.row_factory = namedtuple_factory

        self.facilities: dict = {}

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        cursor = self.cxn.cursor()

        # Load the petrochemicals
        for row in cursor.execute('SELECT * FROM facility_master'):
            print(row)
