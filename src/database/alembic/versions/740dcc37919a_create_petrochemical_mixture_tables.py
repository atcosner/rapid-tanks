"""Create petrochemical mixture tables

Revision ID: 740dcc37919a
Revises: ff432bacb924
Create Date: 2024-02-08 19:12:12.704932

"""
from alembic import op
from typing import Sequence

from src.database.definitions import OrmBase
from src.database.definitions.mixture import PetrochemicalMixture, PetrochemicalAssociation


# revision identifiers, used by Alembic.
revision: str = '740dcc37919a'
down_revision: str | None = 'ff432bacb924'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(
        bind=op.get_bind(),
        tables=[PetrochemicalMixture.__table__, PetrochemicalAssociation.__table__],
    )


def downgrade() -> None:
    OrmBase.metadata.drop_all(
        bind=op.get_bind(),
        tables=[PetrochemicalMixture.__table__, PetrochemicalAssociation.__table__],
    )