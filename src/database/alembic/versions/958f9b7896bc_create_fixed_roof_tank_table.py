"""Create fixed roof tank table

Revision ID: 958f9b7896bc
Revises: 812a6802979b
Create Date: 2024-02-04 12:53:23.694012

"""
from alembic import op
from typing import Sequence
from sqlalchemy.orm.session import Session

from src.util.enums import InsulationType
from src.database.definitions import OrmBase
from src.database.definitions.tank import FixedRoofTank, FixedRoofType, TankInsulationType


# revision identifiers, used by Alembic.
revision: str = '958f9b7896bc'
down_revision: str | None = '812a6802979b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    OrmBase.metadata.create_all(
        bind=op.get_bind(),
        tables=[FixedRoofTank.__table__, FixedRoofType.__table__, TankInsulationType.__table__],
    )

    # Populate the 2 types of fixed roofs
    with Session(bind=op.get_bind()) as session:
        session.add(FixedRoofType(name='Cone'))
        session.add(FixedRoofType(name='Dome'))
        session.commit()

    # Populate the 3 types of insulation
    with Session(bind=op.get_bind()) as session:
        session.add(TankInsulationType(name=TankInsulationType.NONE))
        session.add(TankInsulationType(name=TankInsulationType.PARTIAL))
        session.add(TankInsulationType(name=TankInsulationType.FULL))
        session.commit()


def downgrade() -> None:
    OrmBase.metadata.drop_all(
        bind=op.get_bind(),
        tables=[FixedRoofTank.__table__, FixedRoofType.__table__, TankInsulationType.__table__],
    )
