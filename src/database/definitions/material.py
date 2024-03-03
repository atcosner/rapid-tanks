from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from . import OrmBase
from.util import PintQuantity


class Petrochemical(MappedAsDataclass, OrmBase):
    __tablename__ = "petrochemical"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    cas_number: Mapped[str]
    molecular_weight: Mapped[PintQuantity] = mapped_column(PintQuantity('g/mol'))
    liquid_density: Mapped[PintQuantity] = mapped_column(PintQuantity('lb/gal'), nullable=True)
    true_vapor_pressure: Mapped[PintQuantity] = mapped_column(PintQuantity('psi'))  # @ 60 degF (Absolute PSI)
    vapor_constant_a: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'))
    vapor_constant_b: Mapped[PintQuantity] = mapped_column(PintQuantity('degC'))
    vapor_constant_c: Mapped[PintQuantity] = mapped_column(PintQuantity('degC'))
    min_valid_temperature: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'), nullable=True)
    max_valid_temperature: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'), nullable=True)
    normal_boiling_point: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'), nullable=True)
    working_loss_product_factor: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), default='1')
