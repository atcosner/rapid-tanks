import sqlite3

from .util import BaseSchemaDelta


class Delta0005(BaseSchemaDelta):
    VERSION = 5

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        #
        # Add builtin petroleum liquids from AP 42 Chapter 7 Table 7.1-2
        #
        petroleum_liquids = [
            ['Midcontinent Crude Oil', '50', '207', '7.1', None, None, None, None],
            ['Motor Gasoline RVP 13', '62', '92', '5.6', '3', '11.644', '5043.6', '7.0'],
            ['Motor Gasoline RVP 10', '66', '92', '5.6', '3', '11.724', '5237.3', '5.2'],
            ['Motor Gasoline RVP 7', '68', '92', '5.6', '3', '11.833', '5500.6', '3.5'],
            ['Jet Naphtha', '80', '120', '6.4', None, '11.368', '5784.3', '1.3'],
            ['Jet Kerosene', '130', '162', '7.0', None, '12.390', '8933.0', '0.008'],
            ['No. 2 Fuel Oil', '130', '188', '7.1', None, '12.101', '8907.0', '0.006'],
            ['No. 6 Fuel Oil', '130', '387', '7.9', None, '10.781', '8933.0', '0.002'],
            ['Vacuum Residual Oil', '190', '387', '7.9', None, '10.104', '10475.5', '0.00004'],
        ]

        # Insert them all into the DB
        cursor.executemany(
            """
                INSERT INTO builtin_petroleum_liquids VALUES
                (NULL, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            petroleum_liquids,
        )
