"""Create petrochemical table

Revision ID: 76a6d92ca250
Revises: 163032656b44
Create Date: 2024-02-08 15:25:59.714235

"""
from typing import Sequence
from alembic import op

from src.database.definitions import OrmBase
from src.database.definitions.material import Petrochemical


# revision identifiers, used by Alembic.
revision: str = '76a6d92ca250'
down_revision: str | None = '163032656b44'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(
        bind=op.get_bind(),
        tables=[Petrochemical.__table__],
    )


def downgrade() -> None:
    OrmBase.metadata.drop_all(
        bind=op.get_bind(),
        tables=[Petrochemical.__table__],
    )
