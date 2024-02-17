from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .material import Petrochemical


class PetrochemicalAssociation(OrmBase):
    __tablename__ = "petrochemical_association"

    mixture_id: Mapped[int] = mapped_column(ForeignKey("petrochemical_mixture.id"), primary_key=True)
    material_id: Mapped[int] = mapped_column(ForeignKey("petrochemical.id"), primary_key=True)

    percent: Mapped[str]

    material: Mapped["Petrochemical"] = relationship()


class PetrochemicalMixture(MappedAsDataclass, OrmBase):
    __tablename__ = "petrochemical_mixture"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    components: Mapped[list["PetrochemicalAssociation"]] = relationship(init=False, cascade="all, delete-orphan")
