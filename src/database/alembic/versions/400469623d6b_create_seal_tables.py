"""Create seal tables

Revision ID: 400469623d6b
Revises: 84ac26d07a89
Create Date: 2024-04-05 21:21:04.281097

"""
from alembic import op
from sqlalchemy.orm.session import Session
from typing import Sequence

from src.database.definitions import OrmBase
from src.database.definitions.seal import SealPrimaryType, SealSecondaryType
from src.util.enums import TankConstructionType


# revision identifiers, used by Alembic.
revision: str = '400469623d6b'
down_revision: str | None = '84ac26d07a89'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SEALS = [
    # Average-fitting
    SealPrimaryType(
        name='Mechanical-shoe',
        tank_construction_id=TankConstructionType.WELDED,
        is_tight_fitting=False,
        secondary_types=[
            SealSecondaryType(name='None', k_ra='5.8', k_rb='0.3', n='2.1'),
            SealSecondaryType(name='Shoe-mounted', k_ra='1.6', k_rb='0.3', n='1.6'),
            SealSecondaryType(name='Rim-mounted', k_ra='0.6', k_rb='0.4', n='1.0'),
        ],
    ),
    SealPrimaryType(
        name='Liquid-mounted',
        tank_construction_id=TankConstructionType.WELDED,
        is_tight_fitting=False,
        secondary_types=[
            SealSecondaryType(name='None', k_ra='1.6', k_rb='0.3', n='1.5'),
            SealSecondaryType(name='Weather shield', k_ra='0.7', k_rb='0.3', n='1.2'),
            SealSecondaryType(name='Rim-mounted', k_ra='0.3', k_rb='0.6', n='0.3'),
        ],
    ),
    SealPrimaryType(
        name='Vapor-mounted',
        tank_construction_id=TankConstructionType.WELDED,
        is_tight_fitting=False,
        secondary_types=[
            SealSecondaryType(name='None', k_ra='6.7', k_rb='0.2', n='3.0'),
            SealSecondaryType(name='Weather Shield', k_ra='3.3', k_rb='0.1', n='3.0'),
            SealSecondaryType(name='Rim-mounted', k_ra='2.2', k_rb='0.003', n='4.3'),
        ],
    ),
    SealPrimaryType(
        name='Mechanical-shoe',
        tank_construction_id=TankConstructionType.RIVETED,
        is_tight_fitting=False,
        secondary_types=[
            SealSecondaryType(name='None', k_ra='10.8', k_rb='0.4', n='2.0'),
            SealSecondaryType(name='Shoe-mounted', k_ra='9.2', k_rb='0.2', n='1.9'),
            SealSecondaryType(name='Rim-mounted', k_ra='1.1', k_rb='0.3', n='1.5'),
        ],
    ),

    # Tight-fitting
    SealPrimaryType(
        name='Mechanical-shoe',
        tank_construction_id=TankConstructionType.WELDED,
        is_tight_fitting=True,
        secondary_types=[
            SealSecondaryType(name='None', k_ra='1.5', k_rb='0.4', n='1.9'),
            SealSecondaryType(name='Shoe-mounted', k_ra='1.0', k_rb='0.4', n='1.5'),
            SealSecondaryType(name='Rim-mounted', k_ra='0.4', k_rb='0.4', n='1.0'),
        ],
    ),
    SealPrimaryType(
        name='Liquid-mounted',
        tank_construction_id=TankConstructionType.WELDED,
        is_tight_fitting=True,
        secondary_types=[
            SealSecondaryType(name='None', k_ra='1.0', k_rb='0.08', n='1.8'),
            SealSecondaryType(name='Weather shield', k_ra='0.4', k_rb='0.2', n='1.3'),
            SealSecondaryType(name='Rim-mounted', k_ra='0.2', k_rb='0.4', n='0.4'),
        ],
    ),
    SealPrimaryType(
        name='Vapor-mounted',
        tank_construction_id=TankConstructionType.WELDED,
        is_tight_fitting=True,
        secondary_types=[
            SealSecondaryType(name='None', k_ra='5.6', k_rb='0.2', n='2.4'),
            SealSecondaryType(name='Weather Shield', k_ra='2.8', k_rb='0.1', n='2.3'),
            SealSecondaryType(name='Rim-mounted', k_ra='2.2', k_rb='0.02', n='2.6'),
        ],
    ),
]


def upgrade() -> None:
    OrmBase.metadata.create_all(
        bind=op.get_bind(),
        tables=[SealPrimaryType.__table__, SealSecondaryType.__table__],
    )

    # Add in the fittings from table 7.1-12
    with Session(bind=op.get_bind()) as session:
        session.add_all(SEALS)
        session.commit()


def downgrade() -> None:
    OrmBase.metadata.drop_all(
        bind=op.get_bind(),
        tables=[SealPrimaryType.__table__, SealSecondaryType.__table__],
    )