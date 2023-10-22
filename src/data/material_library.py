import sqlite3
from pathlib import Path

BASE_DB_PATH = Path('~/PycharmProjects/rapid-tanks/src/data/database/base_db').expanduser()


class MaterialLibrary:
    def __init__(self, db_path: Path | None = None, autoload: bool = True):
        self._db_path = db_path if db_path is not None else BASE_DB_PATH

        if not self._db_path.exists():
            raise Exception(f'DB did not exist! ({self._db_path})')

        if autoload:
            pass

    def load_from_db(self) -> None:
        pass
