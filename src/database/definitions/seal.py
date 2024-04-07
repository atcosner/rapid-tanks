from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .util import PintQuantity


class SealSecondaryType(MappedAsDataclass, OrmBase):
    __tablename__ = "seal_secondary_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    k_ra: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'))  # lb-mole/ft-yr
    k_rb: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)  # lb-mole/[(mph)^n-ft-yr]
    n: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)

    primary_type_id = mapped_column(ForeignKey("seal_primary_type.id"))
    primary_type: Mapped["SealPrimaryType"] = relationship(init=False, back_populates="secondary_types")


class SealPrimaryType(MappedAsDataclass, OrmBase):
    __tablename__ = "seal_primary_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    tank_construction_id: Mapped[int]
    is_tight_fitting: Mapped[bool]

    secondary_types: Mapped[list[SealSecondaryType]] = relationship(back_populates="primary_type")
