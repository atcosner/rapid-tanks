from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .util import PintQuantity


class FittingSecondaryType(MappedAsDataclass, OrmBase):
    __tablename__ = "fitting_secondary_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    k_fa: Mapped[PintQuantity] = mapped_column(PintQuantity('mol/yr'))
    k_fb: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)  # mole/[(mph)^M * yr]
    m: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'), nullable=True)

    primary_type_id = mapped_column(ForeignKey("fitting_primary_type.id"))
    primary_type: Mapped["FittingPrimaryType"] = relationship(init=False, back_populates="secondary_types")


class FittingPrimaryType(MappedAsDataclass, OrmBase):
    __tablename__ = "fitting_primary_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    secondary_types: Mapped[list[FittingSecondaryType]] = relationship(back_populates="primary_type")


class IfrtFittingAssociation(MappedAsDataclass, OrmBase):
    __tablename__ = "ifrt_fitting_association"

    quantity: Mapped[int]
    tank_id: Mapped[int] = mapped_column(ForeignKey("internal_floating_roof_tank.id"), primary_key=True, init=False)
    fitting_id: Mapped[int] = mapped_column(ForeignKey("fitting_secondary_type.id"), primary_key=True, init=False)

    fitting: Mapped["FittingSecondaryType"] = relationship()
    tank: Mapped["InternalFloatingRoofTank"] = relationship(init=False, back_populates="fittings")
