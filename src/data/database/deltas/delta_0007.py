import sqlite3

from .util import BaseSchemaDelta


class Delta0007(BaseSchemaDelta):
    VERSION = 7

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        # Add in tables to store facility settings
        cursor.execute("""
            CREATE TABLE facility_master(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT,
                description TEXT,
                company TEXT,
                meteorological_site_id INTEGER,
                
                FOREIGN KEY(meteorological_site_id) REFERENCES meteorological_site(id)
            );
        """)
