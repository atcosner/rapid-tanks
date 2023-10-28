import sqlite3
from pathlib import Path
from typing import NamedTuple

from src.constants.material import Material, Petrochemical, PetroleumLiquid
from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory


class MaterialKey(NamedTuple):
    name: str
    is_custom: bool


class MaterialLibrary:
    def __init__(self, db_path: Path | None = None, autoload: bool = True):
        self._db_path = db_path if db_path is not None else DEV_DB_FILE_PATH

        self.petrochemicals: dict[MaterialKey, Material] = {}
        self.petroleum_liquids: dict[MaterialKey, Material] = {}

        if not self._db_path.exists():
            raise Exception(f'DB does not exist! ({self._db_path})')

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        # Connect to the DB
        cxn = sqlite3.connect(self._db_path)
        cxn.row_factory = namedtuple_factory

        cursor = cxn.cursor()

        # Load the petrochemicals
        for row in cursor.execute('SELECT * FROM builtin_petrochemicals'):
            self.petrochemicals[MaterialKey(row.name, False)] = Petrochemical.from_namedtuple(row)
        for row in cursor.execute('SELECT * FROM custom_petrochemicals'):
            self.petrochemicals[MaterialKey(row.name, True)] = Petrochemical.from_namedtuple(row)

        # Load the petroleum liquids
        for row in cursor.execute('SELECT * FROM builtin_petroleum_liquids'):
            self.petroleum_liquids[MaterialKey(row.name, False)] = PetroleumLiquid.from_namedtuple(row)
        for row in cursor.execute('SELECT * FROM custom_petroleum_liquids'):
            self.petroleum_liquids[MaterialKey(row.name, True)] = PetroleumLiquid.from_namedtuple(row)

    def get_material(self, name: str) -> Material | None:
        # TODO: What should we do if a name exists in both?
        # TODO: Differences in cases?

        for key, material in self.petrochemicals.items():
            if key.name == name:
                return material

        for key, material in self.petroleum_liquids.items():
            if key.name == name:
                return material

        return None
