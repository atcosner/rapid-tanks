from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.database import DEV_DB_FILE_PATH
from src.database.definitions import OrmBase
from src.database.definitions.facility import Facility

# # Delete the DB file
# DEV_DB_FILE_PATH.unlink(missing_ok=True)

# Create an engine
engine = create_engine(f'sqlite+pysqlite:///{DEV_DB_FILE_PATH}', echo=True)

# Create all the tables we have declared
OrmBase.metadata.create_all(engine)

session = Session(engine)

# # Insert a test facility
# test_facility = Facility(name='Test1', description='TEST FACILITY - 1', company='T1')
# session.add(test_facility)
# session.commit()

facility = session.get(Facility, 1)
print(facility)
print(facility.fixed_roof_tanks[0])

# # Create a tank for this facility
# facility.fixed_roof_tanks.append(
#     FixedRoofTank(
#         name='Fixed Roof Tank 1',
#         description='New testing tank',
#         is_vertical=False,
#
#         shell_height='6',
#         shell_diameter='12',
#         #shell_color_id = mapped_column(ForeignKey("paint_color.id"))
#         #shell_condition_id = mapped_column(ForeignKey("paint_condition.id"))
#
#         roof_type='Dome',
#         #roof_color_id = mapped_column(ForeignKey("paint_color.id"))
#         #roof_condition_id = mapped_column(ForeignKey("paint_condition.id"))
#         roof_height='4',
#         roof_slope='0.625',
#         roof_radius='4',
#
#         vent_vacuum_setting='-0.003',
#         vent_breather_setting='0.003',
#
#         maximum_liquid_height='10',
#         average_liquid_height='8',
#         working_volume='11',
#         turnovers_per_year='5',
#         net_throughput='5000',
#         is_heated=False,
#     )
# )
#
# print(facility in session.dirty)
# print(session.new)
# session.commit()
