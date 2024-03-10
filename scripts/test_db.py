import calendar
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.util.enums import MixtureMakeupType, InsulationType
from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.material import Petrochemical
from src.database.definitions.meteorological import MeteorologicalSite
from src.database.definitions.mixture import PetrochemicalMixture, PetrochemicalAssociation
from src.database.definitions.paint import PaintColor, PaintCondition
from src.database.definitions.service_record import ServiceRecord
from src.database.definitions.tank import FixedRoofTank, FixedRoofType, TankInsulationType
from src.gui.widgets.util.constants import MONTH_NAMES


with Session(DB_ENGINE) as session:
    # Sample Calculation #1
    meteorological_site = session.scalar(select(MeteorologicalSite).where(MeteorologicalSite.name == 'Denver'))
    white_paint = session.scalar(select(PaintColor).where(PaintColor.name == 'White'))
    average_condition = session.scalar(select(PaintCondition).where(PaintCondition.name == 'Average'))
    cone_roof = session.scalar(select(FixedRoofType).where(FixedRoofType.name == 'Cone'))
    uninsulated = session.scalar(select(TankInsulationType).where(TankInsulationType.name == InsulationType.NONE))

    benzene = session.scalar(select(Petrochemical).where(Petrochemical.name == 'Benzene'))
    toluene = session.scalar(select(Petrochemical).where(Petrochemical.name == 'Toluene'))
    cyclohexane = session.scalar(select(Petrochemical).where(Petrochemical.name == 'Cyclohexane'))

    sc1_mixture = PetrochemicalMixture(
        name='SC #1 Mixture',
        makeup_type_id=MixtureMakeupType.WEIGHT,
    )
    sc1_mixture.components.append(PetrochemicalAssociation(value='2812', material=benzene))
    sc1_mixture.components.append(PetrochemicalAssociation(value='258', material=toluene))
    sc1_mixture.components.append(PetrochemicalAssociation(value='101', material=cyclohexane))

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
    sc1_tank.insulation = uninsulated

    for idx, name in enumerate(MONTH_NAMES):
        record = ServiceRecord(
            start_date=date(year=2024, month=idx + 1, day=1),
            end_date=date(year=2024, month=idx + 1, day=calendar.monthrange(2024, idx + 1)[1]),
            throughput='704.17',
        )
        record.mixture = sc1_mixture
        sc1_tank.service_records.append(record)

    sc1_facility = Facility(
        name='Sample Calculation #1',
        description='',
        company='',
    )
    sc1_facility.site = meteorological_site
    sc1_facility.fixed_roof_tanks.append(sc1_tank)

    session.add(sc1_facility)
    session.commit()
