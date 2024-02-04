"""Create meteorological tables

Revision ID: a1b1fc1ce435
Revises: c4d3f45b53f2
Create Date: 2024-02-04 12:28:22.778022

"""
from typing import Sequence
from alembic import op

from src.database.definitions import OrmBase
from src.database.definitions.meteorological import MeteorologicalSite, MeteorologicalMonthRecord


# revision identifiers, used by Alembic.
revision: str = 'a1b1fc1ce435'
down_revision: str | None = 'c4d3f45b53f2'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(
        bind=op.get_bind(),
        tables=[MeteorologicalSite.__table__, MeteorologicalMonthRecord.__table__],
    )


def downgrade() -> None:
    OrmBase.metadata.drop_all(
        bind=op.get_bind(),
        tables=[MeteorologicalSite.__table__, MeteorologicalMonthRecord.__table__],
    )
