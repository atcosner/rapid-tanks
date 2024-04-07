import calendar
from datetime import date
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.util.enums import MixtureMakeupType, InsulationType, TankConstructionType
from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.fittings import FittingPrimaryType, FittingSecondaryType, IfrtFittingAssociation
from src.database.definitions.material import Petrochemical
from src.database.definitions.meteorological import MeteorologicalSite
from src.database.definitions.mixture import Mixture, MixtureAssociation
from src.database.definitions.paint import PaintColor, PaintCondition
from src.database.definitions.seal import SealPrimaryType
from src.database.definitions.service_record import FrtServiceRecord, IfrtServiceRecord
from src.database.definitions.fixed_roof_tank import FixedRoofTank, FixedRoofType, TankInsulationType
from src.database.definitions.floating_roof_tank import InternalFloatingRoofTank
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

    sc1_mixture = Mixture(
        name='SC #1 Mixture',
        makeup_type_id=MixtureMakeupType.WEIGHT,
    )
    sc1_mixture.components.append(MixtureAssociation(value='2812', petrochemical=benzene, petroleum_liquid=None))
    sc1_mixture.components.append(MixtureAssociation(value='258', petrochemical=toluene, petroleum_liquid=None))
    sc1_mixture.components.append(MixtureAssociation(value='101', petrochemical=cyclohexane, petroleum_liquid=None))

    # SC #1 Tank
    sc1_tank = FixedRoofTank(
        name='VFRT #1',
        shell_height='12',
        shell_diameter='6',
        roof_radius='3',
        maximum_liquid_height='11.5',
        minimum_liquid_height='4.5',
        net_throughput='8450',
    )
    sc1_tank.shell_paint_color = white_paint
    sc1_tank.shell_paint_condition = average_condition
    sc1_tank.roof_paint_color = white_paint
    sc1_tank.roof_paint_condition = average_condition
    sc1_tank.roof_type = cone_roof
    sc1_tank.insulation = uninsulated

    month_throughput = Decimal(sc1_tank.net_throughput) / 12
    for idx, name in enumerate(MONTH_NAMES):
        record = FrtServiceRecord(
            start_date=date(year=2024, month=idx + 1, day=1),
            end_date=date(year=2024, month=idx + 1, day=calendar.monthrange(2024, idx + 1)[1]),
            throughput=str(month_throughput.quantize(Decimal('1.00'))),
        )
        record.mixture = sc1_mixture
        sc1_tank.service_records.append(record)

    # Sample Calculation #2
    sc2_tank = FixedRoofTank(
        name='HFRT #1',
        shell_height='12',
        shell_diameter='6',
        maximum_liquid_height='11.5',
        minimum_liquid_height='4.5',
        net_throughput='8450',
        is_vertical=False,
    )
    sc2_tank.shell_paint_color = white_paint
    sc2_tank.shell_paint_condition = average_condition
    sc2_tank.roof_paint_color = white_paint
    sc2_tank.roof_paint_condition = average_condition
    sc2_tank.insulation = uninsulated

    month_throughput = Decimal(sc1_tank.net_throughput) / 12
    for idx, name in enumerate(MONTH_NAMES):
        record = FrtServiceRecord(
            start_date=date(year=2024, month=idx + 1, day=1),
            end_date=date(year=2024, month=idx + 1, day=calendar.monthrange(2024, idx + 1)[1]),
            throughput=str(month_throughput.quantize(Decimal('1.00'))),
        )
        record.mixture = sc1_mixture
        sc2_tank.service_records.append(record)

    sc1_facility = Facility(
        name='Sample Calculation #1 and #2',
        description='',
        company='',
    )
    sc1_facility.site = meteorological_site
    sc1_facility.fixed_roof_tanks.append(sc1_tank)
    sc1_facility.fixed_roof_tanks.append(sc2_tank)

    session.add(sc1_facility)
    session.commit()

    # Sample Calculation #4
    sc4_site = session.scalar(select(MeteorologicalSite).where(MeteorologicalSite.name == 'Tulsa'))
    sc4_primary_seal = session.scalar(
        select(SealPrimaryType)
        .where(SealPrimaryType.name == 'Liquid-mounted')
        .where(SealPrimaryType.tank_construction_id == TankConstructionType.WELDED)
        .where(SealPrimaryType.is_tight_fitting == False)
    )
    for secondary_type in sc4_primary_seal.secondary_types:
        if secondary_type.name == 'Rim-mounted':
            sc4_seal = secondary_type

    SC4_FITTINGS = [
        ('Access Hatch', 'Unbolted cover, ungasketed', 2),
    ]
    fittings = []
    for primary, secondary, quantity in SC4_FITTINGS:
        primary_type = session.scalar(select(FittingPrimaryType).where(FittingPrimaryType.name == primary))
        secondary_type = session.scalar(
            select(FittingSecondaryType)
            .where(FittingSecondaryType.primary_type_id == primary_type.id)
            .where(FittingSecondaryType.name == secondary)
        )

        fittings.append(
            IfrtFittingAssociation(
                fitting=secondary_type,
                quantity=quantity,
            )
        )

    sc4_tank = InternalFloatingRoofTank(
        name='IFRT #1',
        description='',
        shell_height='35',
        shell_diameter='70',
        autofill_support_column_count=False,
        support_column_count='1',
    )
    sc4_tank.shell_paint_color = white_paint
    sc4_tank.shell_paint_condition = average_condition
    sc4_tank.roof_paint_color = white_paint
    sc4_tank.roof_paint_condition = average_condition
    sc4_tank.seal = sc4_seal
    sc4_tank.fittings = fittings

    monthly_sum_liquid_decrease = Decimal(1735) / 12
    for idx, name in enumerate(MONTH_NAMES):
        record = IfrtServiceRecord(
            start_date=date(year=2024, month=idx + 1, day=1),
            end_date=date(year=2024, month=idx + 1, day=calendar.monthrange(2024, idx + 1)[1]),
            sum_liquid_level_decrease=str(monthly_sum_liquid_decrease.quantize(Decimal('1.00'))),
            throughput=None,
        )
        sc4_tank.service_records.append(record)

    sc4_facility = Facility(name='Sample Calculation #4', description='', company='')
    sc4_facility.site = sc4_site
    sc4_facility.internal_floating_roof_tanks.append(sc4_tank)
    session.add(sc4_facility)
    session.commit()
