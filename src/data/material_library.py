import sqlite3
from pathlib import Path

from src.constants.material import Material, OrganicLiquid
from src.data.database import DEV_DB_FILE_PATH
from src.util.database import namedtuple_factory


class MaterialLibrary:
    def __init__(self, db_path: Path | None = None, autoload: bool = True):
        self._db_path = db_path if db_path is not None else DEV_DB_FILE_PATH

        self.builtin_materials: dict[str, Material] = {}
        self.custom_materials: dict[str, Material] = {}

        if not self._db_path.exists():
            raise Exception(f'DB does not exist! ({self._db_path})')

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        # Connect to the DB
        cxn = sqlite3.connect(self._db_path)
        cxn.row_factory = namedtuple_factory

        cursor = cxn.cursor()

        # Query the DB for materials to load
        for row in cursor.execute('SELECT * FROM builtin_organic_liquids'):
            self.builtin_materials[row.name] = OrganicLiquid.from_namedtuple(row)

        for row in cursor.execute('SELECT * FROM custom_organic_liquids'):
            self.custom_materials[row.name] = OrganicLiquid.from_namedtuple(row)

    def get_material(self, name: str) -> Material | None:
        # TODO: What should we do if a name exists in both?
        # TODO: Differences in cases?

        if name in self.builtin_materials:
            return self.builtin_materials[name]

        if name in self.custom_materials:
            return self.custom_materials[name]

        return None

    def get_material_keys(self, custom: bool = False) -> list[tuple[str, str]]:
        data = self.custom_materials if custom else self.builtin_materials
        return [(name, material.cas_number) for name, material in data.items()]
