"""Create internal floating roof tank table

Revision ID: 97a1251151c8
Revises: 400469623d6b
Create Date: 2024-04-06 13:02:22.541884

"""
from alembic import op
from typing import Sequence

from src.database.definitions import OrmBase
from src.database.definitions.floating_roof_tank import InternalFloatingRoofTank


# revision identifiers, used by Alembic.
revision: str = '97a1251151c8'
down_revision: str | None = '400469623d6b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(bind=op.get_bind(), tables=[InternalFloatingRoofTank.__table__])


def downgrade() -> None:
    OrmBase.metadata.drop_all(bind=op.get_bind(), tables=[InternalFloatingRoofTank.__table__])
