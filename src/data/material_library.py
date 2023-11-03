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
    def __init__(self, db_location: Path | sqlite3.Connection | None = None, autoload: bool = True):
        # Figure out where the DB is
        if db_location is None:
            self.cxn = sqlite3.connect(DEV_DB_FILE_PATH)
        elif isinstance(db_location, Path):
            self.cxn = sqlite3.connect(db_location)
        elif isinstance(db_location, sqlite3.Connection):
            self.cxn = db_location
        else:
            raise RuntimeError(f'Unknown DB location type! {type(db_location)}')

        # Use our namedtuple row factory
        self.cxn.row_factory = namedtuple_factory

        self.petrochemicals: dict[MaterialKey, Material] = {}
        self.petroleum_liquids: dict[MaterialKey, Material] = {}

        if autoload:
            self.load_from_db()

    def load_from_db(self) -> None:
        cursor = self.cxn.cursor()

        # Load the petrochemicals
        for row in cursor.execute('SELECT * FROM builtin_petrochemicals'):
            self.petrochemicals[MaterialKey(row.name, False)] = Petrochemical.from_db_row(row)
        for row in cursor.execute('SELECT * FROM custom_petrochemicals'):
            self.petrochemicals[MaterialKey(row.name, True)] = Petrochemical.from_db_row(row)

        # Load the petroleum liquids
        for row in cursor.execute('SELECT * FROM builtin_petroleum_liquids'):
            self.petroleum_liquids[MaterialKey(row.name, False)] = PetroleumLiquid.from_db_row(row)
        for row in cursor.execute('SELECT * FROM custom_petroleum_liquids'):
            self.petroleum_liquids[MaterialKey(row.name, True)] = PetroleumLiquid.from_db_row(row)

    def store_material(self, material: Material) -> None:
        # Handle the material depending on what it is
        with self.cxn:
            material_row = material.to_db_row()

            if isinstance(material, Petrochemical):
                self.petrochemicals[MaterialKey(material.name, True)] = material
                self.cxn.execute(f'INSERT INTO custom_petrochemicals VALUES {material_row}')
            elif isinstance(material, PetroleumLiquid):
                self.petroleum_liquids[MaterialKey(material.name, True)] = material
                self.cxn.execute(f'INSERT INTO custom_petroleum_liquids VALUES {material_row}')
            else:
                raise Exception(f'Unknown material type! {type(material)}')

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


