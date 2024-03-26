from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .util import PintQuantity


class FittingSubType(MappedAsDataclass, OrmBase):
    __tablename__ = "fitting_sub_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    fitting_type_id = mapped_column(ForeignKey("fitting_type.id"))

    k_fa: Mapped[PintQuantity] = mapped_column(PintQuantity('mol/yr'))
    k_fb: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)  # mole/[(mph)^M * yr]
    m: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)
    internal_default: Mapped[bool] = mapped_column(default=False)
    external_default: Mapped[bool] = mapped_column(default=False)

    parent_type: Mapped["FittingType"] = relationship(init=False, back_populates="sub_types")


class FittingType(MappedAsDataclass, OrmBase):
    __tablename__ = "fitting_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    typical_count: Mapped[int] = mapped_column(nullable=True)

    sub_types: Mapped[list[FittingSubType]] = relationship(back_populates="parent_type")


class Fitting(MappedAsDataclass, OrmBase):
    __tablename__ = "fitting"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    fitting_type_id = mapped_column(ForeignKey("fitting_type.id"))
    fitting_sub_type_id = mapped_column(ForeignKey("fitting_sub_type.id"))

    fitting_type: Mapped[FittingType] = relationship()
    fitting_sub_type: Mapped[FittingSubType] = relationship()
