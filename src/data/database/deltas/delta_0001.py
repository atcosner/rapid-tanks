import sqlite3

from . import BaseSchemaDelta, SchemaUpdate


@SchemaUpdate(version=1)
class Delta0001(BaseSchemaDelta):
    def upgrade(self, cxn: sqlite3.Cursor) -> None:
        # Add the version table
        cxn.execute("""
            CREATE TABLE version(
                id INTEGER,
                update_ts TEXT
            );
        """)
