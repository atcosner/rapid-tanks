from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .util import PintQuantity


class FittingSubType(MappedAsDataclass, OrmBase):
    __tablename__ = "fitting_sub_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    k_fa: Mapped[PintQuantity] = mapped_column(PintQuantity('mol/yr'))
    k_fb: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)  # mole/[(mph)^M * yr]
    m: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)
    internal_default: Mapped[bool] = mapped_column(default=False)
    external_default: Mapped[bool] = mapped_column(default=False)


class Fitting(MappedAsDataclass, OrmBase):
    __tablename__ = "fitting"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    typical_count: Mapped[int] = mapped_column(nullable=True)

    sub_types: Mapped[list[FittingSubType]] = relationship()
