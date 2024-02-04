"""Create facility table

Revision ID: 812a6802979b
Revises: a1b1fc1ce435
Create Date: 2024-02-04 12:39:57.187079

"""
from typing import Sequence
from alembic import op

from src.database.definitions import OrmBase
import src.database.definitions.tank  # Import this so Facility knows about the fixed roof tank
from src.database.definitions.facility import Facility


# revision identifiers, used by Alembic.
revision: str = '812a6802979b'
down_revision: str | None = 'a1b1fc1ce435'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(bind=op.get_bind(), tables=[Facility.__table__])


def downgrade() -> None:
    OrmBase.metadata.drop_all(bind=op.get_bind(), tables=[Facility.__table__])
