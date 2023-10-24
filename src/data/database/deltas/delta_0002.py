import sqlite3

from .util import BaseSchemaDelta


class Delta0002(BaseSchemaDelta):
    VERSION = 2

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        # Add the builtin materials table
        cursor.execute("""
            CREATE TABLE builtin_organic_liquids(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT,
                cas_number TEXT,
                molecular_weight TEXT,
                liquid_density TEXT,
                true_vapor_pressure TEXT,
                antoine_a TEXT,
                antoine_b TEXT,
                antoine_c TEXT,
                antoine_min_temp TEXT,
                antoine_max_temp TEXT,
                normal_boiling_point TEXTs
            );
        """)

        # Create the custom materials table with the same schema
        row = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='builtin_organic_liquids'")
        create_sql = row.fetchone()[0].replace('builtin_organic_liquids', 'custom_organic_liquids')
        cursor.execute(create_sql)
