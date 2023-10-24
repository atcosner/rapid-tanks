import sqlite3

from .util import BaseSchemaDelta


class Delta0003(BaseSchemaDelta):
    VERSION = 3

    def upgrade(self, cursor: sqlite3.Cursor) -> None:
        # Insert the builtin materials from AP 42 Chapter 7 Table 7.1-3
        pass
