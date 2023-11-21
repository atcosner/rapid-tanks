import sqlite3

from .util import BaseSchemaDelta


class Delta0008(BaseSchemaDelta):
    VERSION = 8

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        #
        # Paint Condition
        #

        cursor.execute("""
            CREATE TABLE paint_condition(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT
            );
        """)

        cursor.execute("""
            INSERT INTO
                paint_condition
            VALUES
                (NULL, 'New'),
                (NULL, 'Average'),
                (NULL, 'Aged');
        """)

        #
        # Paint Color
        #

        cursor.execute("""
            CREATE TABLE paint_color(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT,

                absorption_new TEXT,
                absorption_average TEXT,
                absorption_aged TEXT
            );
        """)

        colors = [
            ('White', '0.17', '0.25', '0.34'),
            ('Aluminum (Specular)', '0.39', '0.44', '0.49'),
            ('Aluminum (Diffuse)', '0.60', '0.64', '0.68'),
            ('Beige', '0.35', '0.42', '0.49'),
            ('Black', '0.97', '0.97', '0.97'),
            ('Brown', '0.58', '0.62', '0.67'),
            ('Gray (Light)', '0.54', '0.58', '0.63'),
            ('Gray (Medium)', '0.68', '0.71', '0.74'),
            ('Green (Dark)', '0.89', '0.90', '0.91'),
            ('Red', '0.89', '0.90', '0.91'),
            ('Rust', '0.38', '0.44', '0.50'),
            ('Tan', '0.43', '0.49', '0.55'),
            ('Unpainted', '0.10', '0.12', '0.15'),

            # Unknown tank colors can be assumed to be white (AP 42 Chapter 7 - Reference 22)
            ('Unknown', '0.17', '0.25', '0.34'),
        ]
        cursor.executemany(
            """
                INSERT INTO paint_color VALUES
                (NULL, ?, ?, ?, ?)
            """,
            colors,
        )

        #
        # Roof Type
        #

        cursor.execute("""
            CREATE TABLE fixed_roof_type(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT
            );
        """)

        cursor.execute("""
            INSERT INTO
                fixed_roof_type
            VALUES
                (NULL, 'Cone'),
                (NULL, 'Dome');
        """)
