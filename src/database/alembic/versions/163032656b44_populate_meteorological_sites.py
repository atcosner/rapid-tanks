"""Populate meteorological sites

Revision ID: 163032656b44
Revises: 958f9b7896bc
Create Date: 2024-02-04 12:56:20.875237

"""
from alembic import op
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from typing import Sequence

from src.database.definitions.meteorological import MeteorologicalSite, MeteorologicalMonthRecord


# revision identifiers, used by Alembic.
revision: str = '163032656b44'
down_revision: str | None = '958f9b7896bc'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    with Session(bind=op.get_bind()) as session:
        for site in session.scalars(select(MeteorologicalSite)).all():
            session.delete(site)
        session.commit()
