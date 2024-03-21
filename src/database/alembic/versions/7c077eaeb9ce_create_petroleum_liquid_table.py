"""Create petroleum liquid table

Revision ID: 7c077eaeb9ce
Revises: a18c8d624cb1
Create Date: 2024-03-20 19:38:10.685101

"""
from alembic import op
from sqlalchemy.orm.session import Session
from typing import Sequence

from src.database.definitions import OrmBase
from src.database.definitions.material import PetroleumLiquid


# revision identifiers, used by Alembic.
revision: str = '7c077eaeb9ce'
down_revision: str | None = 'a18c8d624cb1'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BUILTIN_LIQUIDS = [
    # PetroleumLiquid(  # TODO: This is a template?
    #     name='Midcontinent Crude Oil',
    #     is_custom=False,
    #     reid_vapor_pressure=None,
    #     vapor_molecular_weight='50',
    #     liquid_molecular_weight='207',
    #     liquid_density='7.1',
    #     astm_distillation_slope=None,
    #     vapor_constant_a='-1',  # TODO: A better way to represent that this needs calculated?
    #     vapor_constant_b='-1',
    #     true_vapor_pressure=None,
    # ),
    # PetroleumLiquid(  # TODO: This is a template?
    #     name='Refined Petroleum Stocks',
    #     is_custom=False,
    #     reid_vapor_pressure=None,
    #     vapor_molecular_weight=None,
    #     liquid_molecular_weight=None,
    #     liquid_density=None,
    #     astm_distillation_slope=None,
    #     vapor_constant_a='-1',  # TODO: A better way to represent that this needs calculated?
    #     vapor_constant_b='-1',
    #     true_vapor_pressure=None,
    # ),
    PetroleumLiquid(
        name='Motor Gasoline RVP 13',
        is_custom=False,
        reid_vapor_pressure='13',
        vapor_molecular_weight='62',
        liquid_molecular_weight='92',
        liquid_density='5.6',
        astm_distillation_slope='3.0',
        vapor_constant_a='11.644',
        vapor_constant_b='5043.6',
        true_vapor_pressure='7.0',
    ),
    PetroleumLiquid(
        name='Motor Gasoline RVP 10',
        is_custom=False,
        reid_vapor_pressure='10',
        vapor_molecular_weight='66',
        liquid_molecular_weight='92',
        liquid_density='5.6',
        astm_distillation_slope='3.0',
        vapor_constant_a='11.724',
        vapor_constant_b='5237.3',
        true_vapor_pressure='5.2',
    ),
    PetroleumLiquid(
        name='Motor Gasoline RVP 7',
        is_custom=False,
        reid_vapor_pressure='7',
        vapor_molecular_weight='68',
        liquid_molecular_weight='92',
        liquid_density='5.6',
        astm_distillation_slope='3.0',
        vapor_constant_a='11.833',
        vapor_constant_b='5500.6',
        true_vapor_pressure='3.5',
    ),
    # PetroleumLiquid(  # TODO: This is a template?
    #     name='Light Naphtha RVP 9-14',
    #     is_custom=False,
    #     reid_vapor_pressure=None,
    #     vapor_molecular_weight=None,
    #     liquid_molecular_weight=None,
    #     liquid_density=None,
    #     astm_distillation_slope='3.5',
    #     vapor_constant_a=None,
    #     vapor_constant_b=None,
    #     true_vapor_pressure=None,
    # ),
    # PetroleumLiquid(  # TODO: This is a template?
    #     name='Naphtha RVP 2-8',
    #     is_custom=False,
    #     reid_vapor_pressure=None,
    #     vapor_molecular_weight=None,
    #     liquid_molecular_weight=None,
    #     liquid_density=None,
    #     astm_distillation_slope='2.5',
    #     vapor_constant_a=None,
    #     vapor_constant_b=None,
    #     true_vapor_pressure=None,
    # ),
    # PetroleumLiquid(  # TODO: This is a template?
    #     name='Aviation Gasoline',
    #     is_custom=False,
    #     reid_vapor_pressure=None,
    #     vapor_molecular_weight=None,
    #     liquid_molecular_weight=None,
    #     liquid_density=None,
    #     astm_distillation_slope='2.0',
    #     vapor_constant_a=None,
    #     vapor_constant_b=None,
    #     true_vapor_pressure=None,
    # ),
    PetroleumLiquid(
        name='Jet Naphtha (JP-4)',
        is_custom=False,
        reid_vapor_pressure=None,
        vapor_molecular_weight='80',
        liquid_molecular_weight='120',
        liquid_density='6.4',
        astm_distillation_slope=None,
        vapor_constant_a='11.368',
        vapor_constant_b='5784.3',
        true_vapor_pressure='1.3',
    ),
    PetroleumLiquid(
        name='Jet Kerosene (Jet A)',
        is_custom=False,
        reid_vapor_pressure=None,
        vapor_molecular_weight='130',
        liquid_molecular_weight='162',
        liquid_density='7.0',
        astm_distillation_slope=None,
        vapor_constant_a='12.390',
        vapor_constant_b='8933.0',
        true_vapor_pressure='0.008',
    ),
    PetroleumLiquid(
        name='No. 2 Fuel Oil (Diesel)',
        is_custom=False,
        reid_vapor_pressure=None,
        vapor_molecular_weight='130',
        liquid_molecular_weight='188',
        liquid_density='7.1',
        astm_distillation_slope=None,
        vapor_constant_a='12.101',
        vapor_constant_b='8907.0',
        true_vapor_pressure='0.006',
    ),
    PetroleumLiquid(
        name='No. 6 Fuel Oil',
        is_custom=False,
        reid_vapor_pressure=None,
        vapor_molecular_weight='130',
        liquid_molecular_weight='387',
        liquid_density='7.9',
        astm_distillation_slope=None,
        vapor_constant_a='10.781',
        vapor_constant_b='8933.0',
        true_vapor_pressure='0.002',
    ),
    PetroleumLiquid(
        name='Vacuum Residual Oil',
        is_custom=False,
        reid_vapor_pressure=None,
        vapor_molecular_weight='190',
        liquid_molecular_weight='387',
        liquid_density='7.9',
        astm_distillation_slope=None,
        vapor_constant_a='10.104',
        vapor_constant_b='10475.5',
        true_vapor_pressure='0.00004',
    ),
]


def upgrade() -> None:
    OrmBase.metadata.create_all(bind=op.get_bind(), tables=[PetroleumLiquid.__table__])

    # Add in the liquids from table 7.1-2
    with Session(bind=op.get_bind()) as session:
        for liquid in BUILTIN_LIQUIDS:
            session.add(liquid)
        session.commit()


def downgrade() -> None:
    OrmBase.metadata.drop_all(bind=op.get_bind(), tables=[PetroleumLiquid.__table__])
