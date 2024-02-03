from sqlalchemy import create_engine

from src.data.database.definitions import OrmBase
import src.data.database.definitions.meteorological
import src.data.database.definitions.facility


# Create an engine
engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

# Create all the tables we have declared
OrmBase.metadata.create_all(engine)
