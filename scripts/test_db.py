import sqlite3

from src.data.meteorological_library import MeteorologicalLibrary
from src.data.database import DEV_DB_FILE_PATH
from src.data.database.schema_repository import SchemaRepository
from src.util.logging import configure_root_logger

configure_root_logger()

# Delete the DB if it exists
DEV_DB_FILE_PATH.unlink(missing_ok=True)

# Open a connection
cxn = sqlite3.connect(DEV_DB_FILE_PATH)

repository = SchemaRepository()
repository.upgrade_db(cxn)

# TEMP: Add in a test meteorological site
data = [
    ('Denver', 'Colorado', '0', '0', '12.08', [
        ('1', '19.2', '42.9', '9.2', '764'),
        ('2', '21.7', '45.7', '9.2', '1052'),
        ('3', '28.2', '53.7', '10.3', '1463'),
        ('4', '34.8', '60.1', '11.0', '1779'),
        ('5', '44.7', '70.6', '10.1', '2049'),
        ('6', '53.2', '80.9', '9.6', '2275'),
        ('7', '60.4', '88.0', '9.2', '2213'),
        ('8', '58.7', '85.2', '8.9', '1941'),
        ('9', '49.6', '77.3', '8.9', '1658'),
        ('10', '37.7', '64.0', '9.2', '1216'),
        ('11', '26.7', '51.1', '8.9', '817'),
        ('12', '19.6', '43.0', '9.2', '664'),
        ('13', '37.9', '63.5', '9.4', '1491'),
    ]),
    ('Colorado Springs', 'Colorado', '0', '0', '12.09', [
        ('1', '19.2', '42.9', '9.2', '764'),
        ('2', '21.7', '45.7', '9.2', '1052'),
        ('3', '28.2', '53.7', '10.3', '1463'),
        ('4', '34.8', '60.1', '11.0', '1779'),
        ('5', '44.7', '70.6', '10.1', '2049'),
        ('6', '53.2', '80.9', '9.6', '2275'),
        ('7', '60.4', '88.0', '9.2', '2213'),
        ('8', '58.7', '85.2', '8.9', '1941'),
        ('9', '49.6', '77.3', '8.9', '1658'),
        ('10', '37.7', '64.0', '9.2', '1216'),
        ('11', '26.7', '51.1', '8.9', '817'),
        ('12', '19.6', '43.0', '9.2', '664'),
        ('13', '37.9', '63.5', '9.4', '1491'),
    ]),
]
with cxn:
    # Insert all the initial site records
    site_records = [record[:5] for record in data]
    cxn.executemany(
        """
            INSERT INTO meteorological_location VALUES
            (NULL, ?, ?, ?, ?, ?)
        """,
        site_records
    )

    # Iterate over tha data to add the detailed records
    for record in data:
        # Get the ID of the master row for this data
        site_id = cxn.execute(f"SELECT id from meteorological_location where name = '{record[0]}'").fetchone()[0]

        # Add the detailed records
        cxn.executemany(
            f"""
                INSERT INTO meteorological_location_detail VALUES
                (NULL, {site_id}, ?, ?, ?, ?, ?)
            """,
            record[5]
        )

# Test if the library can load
library = MeteorologicalLibrary()
print(library.get_site(1))
print(library.get_site(2))

# Add a test facility
with cxn:
    cxn.execute(
        f"INSERT INTO facility_master VALUES (NULL, 'TEST - FACILITY', 'TEST', 'LABCORP', 1)"
    )
