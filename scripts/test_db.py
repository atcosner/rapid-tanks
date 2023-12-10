import sqlite3

from src.data.facility_library import FacilityLibrary
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

# Test if the library can load
met_library = MeteorologicalLibrary()
print(met_library.get_site_by_id(1))
print(met_library.get_site_by_id(2))

# Add a test facility
with cxn:
    cxn.execute(
        f"INSERT INTO facility_master VALUES (NULL, 'TEST - FACILITY', 'TEST', 'LABCORP', 1)"
    )

# Test if the library can load
facility_library = FacilityLibrary()
print(facility_library.get_facility_by_id(1))
