import sqlite3
import unittest

from ..material_library import MaterialLibrary
from ..database.deltas.delta_0002 import Delta0002
from ..database.deltas.delta_0004 import Delta0004


class TestMaterialLibrary(unittest.TestCase):
    def setUp(self) -> None:
        # Create the DB
        self.cxn = sqlite3.connect(':memory:')
        self.cursor = self.cxn.cursor()

        # Add the required tables
        Delta0002().upgrade(self.cursor)
        Delta0004().upgrade(self.cursor)

        # Add some materials to the DB
        self.cxn.execute(
            """
                INSERT INTO builtin_petrochemicals VALUES
                (NULL, 'Test - Petro', '12', '72', '84.1', '84', '84', '3.3', '84', '1.1', '84', '84')
            """
        )
        self.cxn.execute(
            """
                INSERT INTO builtin_petroleum_liquids VALUES
                (NULL, 'Test - Liquid', '12', '72', '84', '84', '84', '84', '56')
            """
        )

    def test_load_builtin_materials(self) -> None:
        # Test that we can load our materials without throwing an exception
        MaterialLibrary(self.cxn)
        self.assertTrue(True)

    def test_save_custom_material(self) -> None:
        library = MaterialLibrary(self.cxn)

        # Store a petrochemical
        material = library.get_material('Test - Petro')
        material.name = 'Custom - Petro'
        library.store_material(material)

        # Store a petroleum liquid
        material = library.get_material('Test - Liquid')
        material.name = 'Custom - Liquid'
        library.store_material(material)

        # Ensure we can reload from the DB
        library.load_from_db()
