from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .meteorological import MeteorologicalSite


class Facility(MappedAsDataclass, OrmBase):
    __tablename__ = "facility"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    company: Mapped[str]
    meteorological_site_id = mapped_column(ForeignKey("meteorological_site.id"))

    site: Mapped[MeteorologicalSite] = relationship()
