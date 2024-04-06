"""Create fitting tables

Revision ID: 84ac26d07a89
Revises: 7c077eaeb9ce
Create Date: 2024-03-24 13:00:27.539761

"""
from alembic import op
from sqlalchemy.orm.session import Session
from typing import Sequence

from src.database.definitions import OrmBase
from src.database.definitions.fittings import FittingPrimaryType, FittingSecondaryType


# revision identifiers, used by Alembic.
revision: str = '84ac26d07a89'
down_revision: str | None = '7c077eaeb9ce'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

FITTINGS = [
    FittingPrimaryType(
        name='Access Hatch',
        secondary_types=[
            FittingSecondaryType(name='Bolted cover, gasketed', k_fa='1.6', k_fb='0', m='0'),
            FittingSecondaryType(name='Unbolted cover, ungaskeed', k_fa='36', k_fb='5.9', m='1.2'),
            FittingSecondaryType(name='Unbolted cover, gasketed', k_fa='31', k_fb='5.2', m='1.3'),
        ],
    ),
    FittingPrimaryType(
        name='Fixed Roof Support Column Well',
        secondary_types=[
            FittingSecondaryType(name='Round pipe, ungasketed sliding cover', k_fa='31', k_fb=None, m=None),
            FittingSecondaryType(name='Round pipe, gasketed sliding cover', k_fa='25', k_fb=None, m=None),
            FittingSecondaryType(name='Round pipe, flexible fabric sleeve seal', k_fa='10', k_fb=None, m=None),
            FittingSecondaryType(name='Built-up column, ungasketed sliding cover', k_fa='51', k_fb=None, m=None),
            FittingSecondaryType(name='Built-up column, gasketed sliding cover', k_fa='33', k_fb=None, m=None),
        ],
    ),
]


def upgrade() -> None:
    OrmBase.metadata.create_all(
        bind=op.get_bind(),
        tables=[FittingPrimaryType.__table__, FittingSecondaryType.__table__],
    )

    # Add in the fittings from table 7.1-12
    with Session(bind=op.get_bind()) as session:
        session.add_all(FITTINGS)
        session.commit()


def downgrade() -> None:
    OrmBase.metadata.drop_all(
        bind=op.get_bind(),
        tables=[FittingPrimaryType.__table__, FittingSecondaryType.__table__],
    )
