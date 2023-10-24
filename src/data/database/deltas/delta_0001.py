import sqlite3

from .util import BaseSchemaDelta


class Delta0001(BaseSchemaDelta):
    VERSION = 1

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        # Add the version table
        cursor.execute("""
            CREATE TABLE version(
                id INTEGER,
                update_ts TEXT
            );
        """)
