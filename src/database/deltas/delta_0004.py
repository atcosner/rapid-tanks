import sqlite3

from .util import BaseSchemaDelta


class Delta0004(BaseSchemaDelta):
    VERSION = 4

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        #
        # Add in tables for petroleum liquids
        #

        cursor.execute("""
            CREATE TABLE builtin_petroleum_liquids(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT,
                vapor_molecular_weight TEXT,
                liquid_molecular_weight TEXT,
                liquid_density TEXT,
                astm_d86_distillation_slope TEXT,
                vapor_pressure_eq_a TEXT,
                vapor_pressure_eq_b TEXT,
                true_vapor_pressure TEXT
            );
        """)

        # Create the custom materials table with the same schema
        row = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='builtin_petroleum_liquids'")
        create_sql = row.fetchone()[0].replace('builtin_petroleum_liquids', 'custom_petroleum_liquids')
        cursor.execute(create_sql)
