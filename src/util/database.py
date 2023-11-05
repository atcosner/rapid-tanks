import sqlite3
from collections import namedtuple
from pathlib import Path


def namedtuple_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    cls = namedtuple("Row", fields)
    return cls._make(row)


def get_db_connection(location: Path | sqlite3.Connection) -> sqlite3.Connection:
    if isinstance(location, Path):
        return sqlite3.connect(location)
    elif isinstance(location, sqlite3.Connection):
        return location
    else:
        raise RuntimeError(f'Unknown DB location type! {type(location)}')
