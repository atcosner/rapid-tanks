import sqlite3

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
