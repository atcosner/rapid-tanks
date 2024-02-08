from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from . import OrmBase


class Petrochemical(MappedAsDataclass, OrmBase):
    __tablename__ = "petrochemical"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    cas_number: Mapped[str]
    molecular_weight: Mapped[str]
    liquid_density: Mapped[str]  # lb/gal
    true_vapor_pressure: Mapped[str]  # @ 60 degF, psia
    vapor_constant_a: Mapped[str]  # dimensionless
    vapor_constant_b: Mapped[str]  # degC
    vapor_constant_c: Mapped[str]  # degC
    min_valid_temperature: Mapped[str]  # degF
    max_valid_temperature: Mapped[str]  # degF
    normal_boiling_point: Mapped[str]  # degF
    working_loss_product_factor: Mapped[str] = mapped_column(default='1')  # dimensionless
