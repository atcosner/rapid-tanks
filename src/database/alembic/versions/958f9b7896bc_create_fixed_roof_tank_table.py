"""Create fixed roof tank table

Revision ID: 958f9b7896bc
Revises: 812a6802979b
Create Date: 2024-02-04 12:53:23.694012

"""
from typing import Sequence
from alembic import op

from src.database.definitions import OrmBase
from src.database.definitions.tank import FixedRoofTank


# revision identifiers, used by Alembic.
revision: str = '958f9b7896bc'
down_revision: str | None = '812a6802979b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(bind=op.get_bind(), tables=[FixedRoofTank.__table__])


def downgrade() -> None:
    OrmBase.metadata.drop_all(bind=op.get_bind(), tables=[FixedRoofTank.__table__])
