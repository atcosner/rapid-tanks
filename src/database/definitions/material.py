from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from . import OrmBase
from.util import PintQuantity


class Petrochemical(MappedAsDataclass, OrmBase):
    __tablename__ = "petrochemical"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    cas_number: Mapped[str]
    molecular_weight: Mapped[PintQuantity] = mapped_column(PintQuantity('lb/mol'))  # lb/lb-mole
    liquid_density: Mapped[PintQuantity] = mapped_column(PintQuantity('lb/gal'), nullable=True)
    true_vapor_pressure: Mapped[PintQuantity] = mapped_column(PintQuantity('psi'))  # @ 60 degF (Absolute PSI)
    vapor_constant_a: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'))
    vapor_constant_b: Mapped[PintQuantity] = mapped_column(PintQuantity('degC'))
    vapor_constant_c: Mapped[PintQuantity] = mapped_column(PintQuantity('degC'))
    min_valid_temperature: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'), nullable=True)
    max_valid_temperature: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'), nullable=True)
    normal_boiling_point: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'), nullable=True)
    working_loss_product_factor: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), default='1')
    is_custom: Mapped[bool] = mapped_column(default=False)  # TODO: Fix the alembic revision and remove the default


class PetroleumLiquid(MappedAsDataclass, OrmBase):
    __tablename__ = "petroleum_liquid"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    is_custom: Mapped[bool]

    reid_vapor_pressure: Mapped[PintQuantity] = mapped_column(PintQuantity('psi'), nullable=True)  # @ 100 degF (Absolute PSI)
    vapor_molecular_weight: Mapped[PintQuantity] = mapped_column(PintQuantity('lb/mol'), nullable=True)  # lb/lb-mole
    liquid_molecular_weight: Mapped[PintQuantity] = mapped_column(PintQuantity('lb/mol'), nullable=True)  # lb/lb-mole
    liquid_density: Mapped[PintQuantity] = mapped_column(PintQuantity('lb/gal'), nullable=True)
    astm_distillation_slope: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'), nullable=True)  # degF/<volume %>
    vapor_constant_a: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)
    vapor_constant_b: Mapped[PintQuantity] = mapped_column(PintQuantity('degR'), nullable=True)
    true_vapor_pressure: Mapped[PintQuantity] = mapped_column(PintQuantity('psi'), nullable=True)  # @ 60 degF (Absolute PSI)
