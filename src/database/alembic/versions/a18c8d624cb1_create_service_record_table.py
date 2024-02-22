"""Create service record table

Revision ID: a18c8d624cb1
Revises: 740dcc37919a
Create Date: 2024-02-21 17:49:09.316452

"""
from alembic import op
from typing import Sequence

from src.database.definitions import OrmBase
from src.database.definitions.service_record import ServiceRecord


# revision identifiers, used by Alembic.
revision: str = 'a18c8d624cb1'
down_revision: str | None = '740dcc37919a'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(bind=op.get_bind(), tables=[ServiceRecord.__table__])


def downgrade() -> None:
    OrmBase.metadata.drop_all(bind=op.get_bind(), tables=[ServiceRecord.__table__])
