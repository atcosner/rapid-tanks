from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.meteorological import MeteorologicalSite
from src.database.definitions.paint import PaintColor, PaintCondition
from src.database.definitions.tank import FixedRoofTank, FixedRoofType


with Session(DB_ENGINE) as session:
    # Sample Calculation #1
    meteorological_site = session.scalar(select(MeteorologicalSite).where(MeteorologicalSite.name == 'Denver'))
    white_paint = session.scalar(select(PaintColor).where(PaintColor.name == 'White'))
    average_condition = session.scalar(select(PaintCondition).where(PaintCondition.name == 'Average'))
    cone_roof = session.scalar(select(FixedRoofType).where(FixedRoofType.name == 'Cone'))

    sc1_tank = FixedRoofTank(
        name='Tank 1',
        shell_height='12',
        shell_diameter='6',
        roof_radius='3',
        maximum_liquid_height='11.5',
        average_liquid_height='8',
        working_volume='1480',
        net_throughput='8450',
    )
    sc1_tank.shell_paint_color = white_paint
    sc1_tank.shell_paint_condition = average_condition
    sc1_tank.roof_paint_color = white_paint
    sc1_tank.roof_paint_condition = average_condition
    sc1_tank.roof_type = cone_roof

    sc1_facility = Facility(
        name='Sample Calculation #1',
        description='',
        company='',
    )
    sc1_facility.site = meteorological_site
    sc1_facility.fixed_roof_tanks.append(sc1_tank)

    session.add(sc1_facility)
    session.commit()
