import sqlite3

from .util import BaseSchemaDelta


class Delta0009(BaseSchemaDelta):
    VERSION = 9

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        # Add in a table for fixed roof tanks
        cursor.execute("""
            CREATE TABLE fixed_roof_tank(
                id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
                name TEXT,
                description TEXT,
                facility_id INTEGER,

                shell_height TEXT,
                shell_diameter TEXT,
                shell_color_id INTEGER,
                shell_condition_id INTEGER,
                
                roof_type_id INTEGER,
                roof_color_id INTEGER,
                roof_condition_id INTEGER,
                roof_height TEXT,
                roof_slope TEXT,
                roof_radius TEXT,
                
                vent_vacuum_setting TEXT,
                vent_breather_setting TEXT,
                
                maximum_liquid_height TEXT,
                average_liquid_height TEXT,
                working_volume TEXT,
                turnovers_per_year TEXT,
                net_throughput TEXT,
                is_heated BOOL,

                FOREIGN KEY(facility_id) REFERENCES facility_master(id),
                FOREIGN KEY(shell_color_id) REFERENCES paint_color(id),
                FOREIGN KEY(shell_condition_id) REFERENCES paint_condition(id),
                FOREIGN KEY(roof_type_id) REFERENCES fixed_roof_type(id),
                FOREIGN KEY(roof_color_id) REFERENCES paint_color(id),
                FOREIGN KEY(roof_condition_id) REFERENCES paint_condition(id)
            );
        """)
