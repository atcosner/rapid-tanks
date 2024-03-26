from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass

from . import OrmBase
from .fittings import Fitting


class FloatingRoofTank(MappedAsDataclass, OrmBase):
    __tablename__ = "floating_roof_tank"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default='')
    facility_id = mapped_column(ForeignKey("facility.id"))
    internal_roof: Mapped[bool]

    # Relationships

    facility: Mapped["Facility"] = relationship(init=False, back_populates="floating_roof_tanks")
    fittings: Mapped[list[Fitting]] = relationship(init=False)
