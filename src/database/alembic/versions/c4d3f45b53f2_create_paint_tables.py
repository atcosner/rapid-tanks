"""Create paint tables

Revision ID: c4d3f45b53f2
Revises: 
Create Date: 2024-02-04 11:48:58.350572

"""
from typing import Sequence

from alembic import op
from sqlalchemy.orm.session import Session

from src.database.definitions import OrmBase
from src.database.definitions.paint import PaintColor, PaintCondition, SolarAbsorptance


# revision identifiers, used by Alembic.
revision: str = 'c4d3f45b53f2'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


CONDITIONS = {cond: PaintCondition(name=cond) for cond in ['New', 'Average', 'Aged']}
COLORS = {
    color: PaintColor(name=color) for color in [
        'White',
        'Aluminum - Specular',
        'Aluminum - Diffuse',
        'Beige/Cream',
        'Black',
        'Brown',
        'Light Gray',
        'Medium Gray',
        'Dark Green',
        'Red',
        'Rust',
        'Tan',
        'Unpainted',
        'Unknown',
    ]
}


def upgrade() -> None:
    OrmBase.metadata.create_all(
        bind=op.get_bind(),
        tables=[PaintCondition.__table__, PaintColor.__table__, SolarAbsorptance.__table__],
    )

    # Populate the 3 tables
    with Session(bind=op.get_bind()) as session:
        # Insert the paint conditions
        session.add_all(CONDITIONS.values())
        session.commit()

        # Insert the paint colors
        session.add_all(COLORS.values())
        session.commit()

        # Add the absorptance coefficients
        session.add(SolarAbsorptance(coefficient='0.17', color=COLORS['White'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.25', color=COLORS['White'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.34', color=COLORS['White'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.39', color=COLORS['Aluminum - Specular'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.44', color=COLORS['Aluminum - Specular'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.49', color=COLORS['Aluminum - Specular'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.60', color=COLORS['Aluminum - Diffuse'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.64', color=COLORS['Aluminum - Diffuse'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.68', color=COLORS['Aluminum - Diffuse'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.35', color=COLORS['Beige/Cream'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.42', color=COLORS['Beige/Cream'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.49', color=COLORS['Beige/Cream'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.97', color=COLORS['Black'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.97', color=COLORS['Black'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.97', color=COLORS['Black'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.58', color=COLORS['Brown'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.62', color=COLORS['Brown'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.67', color=COLORS['Brown'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.54', color=COLORS['Light Gray'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.58', color=COLORS['Light Gray'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.63', color=COLORS['Light Gray'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.68', color=COLORS['Medium Gray'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.71', color=COLORS['Medium Gray'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.74', color=COLORS['Medium Gray'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.89', color=COLORS['Dark Green'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.90', color=COLORS['Dark Green'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.91', color=COLORS['Dark Green'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.89', color=COLORS['Red'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.90', color=COLORS['Red'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.91', color=COLORS['Red'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.38', color=COLORS['Rust'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.44', color=COLORS['Rust'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.50', color=COLORS['Rust'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.43', color=COLORS['Tan'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.49', color=COLORS['Tan'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.55', color=COLORS['Tan'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.10', color=COLORS['Unpainted'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.12', color=COLORS['Unpainted'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.15', color=COLORS['Unpainted'], condition=CONDITIONS['Aged']))

        session.add(SolarAbsorptance(coefficient='0.17', color=COLORS['Unknown'], condition=CONDITIONS['New']))
        session.add(SolarAbsorptance(coefficient='0.25', color=COLORS['Unknown'], condition=CONDITIONS['Average']))
        session.add(SolarAbsorptance(coefficient='0.34', color=COLORS['Unknown'], condition=CONDITIONS['Aged']))
        session.commit()


def downgrade() -> None:
    OrmBase.metadata.drop_all(
        bind=op.get_bind(),
        tables=[PaintCondition.__table__, PaintColor.__table__, SolarAbsorptance.__table__],
    )
