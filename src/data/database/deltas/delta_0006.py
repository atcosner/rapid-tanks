import sqlite3

from .util import BaseSchemaDelta


class Delta0006(BaseSchemaDelta):
    VERSION = 6

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        # Add in the master table for meteorological data
        cursor.execute("""
            CREATE TABLE meteorological_location(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT,
                state TEXT,
                gps_latitude TEXT,
                gps_longitude TEXT,
                atmospheric_pressure TEXT
            );
        """)

        # Add in the detail table for meteorological data
        cursor.execute("""
            CREATE TABLE meteorological_location_detail(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                site_id INTEGER,
                month_id INTEGER,
                average_temp_min TEXT,
                average_temp_max TEXT,
                average_wind_speed TEXT,
                average_daily_insolation TEXT,
                
                FOREIGN KEY(site_id) REFERENCES meteorological_location(id)
            );
        """)
