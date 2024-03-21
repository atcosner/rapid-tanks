from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .material import Petrochemical, PetroleumLiquid


class MixtureAssociation(OrmBase):
    __tablename__ = "mixture_association"

    id: Mapped[int] = mapped_column(primary_key=True)
    mixture_id: Mapped[int] = mapped_column(ForeignKey("mixture.id"))

    value: Mapped[str]
    petrochemical_id: Mapped[int] = mapped_column(ForeignKey("petrochemical.id"), nullable=True)
    petroleum_liquid_id: Mapped[int] = mapped_column(ForeignKey("petroleum_liquid.id"), nullable=True)

    petrochemical: Mapped[Petrochemical] = relationship()
    petroleum_liquid: Mapped[PetroleumLiquid] = relationship()


class Mixture(MappedAsDataclass, OrmBase):
    __tablename__ = "mixture"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    makeup_type_id: Mapped[int]

    components: Mapped[list[MixtureAssociation]] = relationship(init=False, cascade="all, delete-orphan")
