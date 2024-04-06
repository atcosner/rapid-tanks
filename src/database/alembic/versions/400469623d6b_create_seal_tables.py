"""Create seal tables

Revision ID: 400469623d6b
Revises: 84ac26d07a89
Create Date: 2024-04-05 21:21:04.281097

"""
from alembic import op
from sqlalchemy.orm.session import Session
from typing import Sequence

from src.database.definitions import OrmBase
from src.database.definitions.seals import SealPrimaryType, SealSecondaryType
from src.util.enums import TankConstructionType


# revision identifiers, used by Alembic.
revision: str = '400469623d6b'
down_revision: str | None = '84ac26d07a89'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

SEALS = [
    SealPrimaryType(
        name='Mechanical-shoe Seal',
        tank_construction_id=TankConstructionType.WELDED,
        is_tight_fitting=False,
        secondary_types=[
            SealSecondaryType(name='Primary only', k_ra='5.8', k_rb='0.3', n='2.1'),
            SealSecondaryType(name='Shoe-mounted Secondary', k_ra='1.6', k_rb='0.3', n='1.6'),
            SealSecondaryType(name='Rim-mounted Secondary', k_ra='0.6', k_rb='0.4', n='1.0'),
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