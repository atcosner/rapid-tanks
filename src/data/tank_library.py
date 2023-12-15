import sqlite3
from pathlib import Path

from src.components.tank import Tank
from src.components.fixed_roof_tank import VerticalFixedRoofTank
from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory, get_db_connection


class TankLibrary:
    def __init__(self, db_location: Path | sqlite3.Connection | None = None, autoload: bool = True):
        # Establish a connection to the DB
        self.cxn = get_db_connection(db_location if db_location is not None else DEV_DB_FILE_PATH)
        self.cxn.row_factory = namedtuple_factory

        self.tanks_by_identifier: dict[str, Tank] = {}

        if autoload:
            self.load_from_db()

    # Allow iterating through the class as if it was the site dict
    def __iter__(self):
        yield from self.tanks_by_identifier.items()

    def load_from_db(self) -> None:
        cursor = self.cxn.cursor()

        # Load the fixed roof tanks
        for row in cursor.execute('SELECT * FROM fixed_roof_tank'):
            if row.is_vertical:
                self.tanks_by_identifier[row.name] = VerticalFixedRoofTank.from_db_row(row)
            else:
                pass

        # TODO: Handle the other types of tanks

    def reload(self) -> None:
        # Remove all existing entries
        self.tanks_by_identifier.clear()

        # Load from the DB
        self.load_from_db()

    def store(self, tank: Tank) -> int | None:
        # Determine which DB table this tank should be stored in
        if isinstance(tank, VerticalFixedRoofTank):
            db_table_name = 'fixed_roof_tank'
        else:
            raise RuntimeError(f'Unknown tank type: {type(tank)}')

        with self.cxn:
            cursor = self.cxn.cursor()
            tank_row = tank.to_db_row()
            cursor.execute(f'INSERT INTO {db_table_name} VALUES {tank_row}')
            return cursor.lastrowid
