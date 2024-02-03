from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.data.database import DEV_DB_FILE_PATH
from src.data.database.definitions import OrmBase
import src.data.database.definitions.facility as facility
import src.data.database.definitions.meteorological
import src.data.database.definitions.paint
import src.data.database.definitions.tank


# Create an engine
engine = create_engine(f'sqlite+pysqlite:///{DEV_DB_FILE_PATH}', echo=True)

# Create all the tables we have declared
OrmBase.metadata.create_all(engine)

session = Session(engine)

# # Insert a test facility
# test_facility = facility.Facility(name='Test1', description='TEST FACILITY - 1', company='T1')
# session.add(test_facility)
# session.commit()

for facility in session.scalars(select(facility.Facility).order_by(facility.Facility.name)).all():
    print(facility)
