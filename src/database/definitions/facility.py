from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .fixed_roof_tank import FixedRoofTank
from .floating_roof_tank import FloatingRoofTank
from .meteorological import MeteorologicalSite


class Facility(MappedAsDataclass, OrmBase):
    __tablename__ = "facility"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    company: Mapped[str]
    meteorological_site_id = mapped_column(ForeignKey("meteorological_site.id"))

    site: Mapped[MeteorologicalSite] = relationship(init=False)
    fixed_roof_tanks: Mapped[list[FixedRoofTank]] = relationship(init=False, back_populates="facility")
    floating_roof_tanks: Mapped[list[FloatingRoofTank]] = relationship(init=False, back_populates="facility")
