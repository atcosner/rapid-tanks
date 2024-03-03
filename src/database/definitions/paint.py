from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .util import PintQuantity


class PaintColor(MappedAsDataclass, OrmBase):
    __tablename__ = "paint_color"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]


class PaintCondition(MappedAsDataclass, OrmBase):
    __tablename__ = "paint_condition"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]


class SolarAbsorptance(MappedAsDataclass, OrmBase):
    __tablename__ = "solar_absorptance"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    color_id = mapped_column(ForeignKey("paint_color.id"))
    condition_id = mapped_column(ForeignKey("paint_condition.id"))
    coefficient: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'))

    color: Mapped[PaintColor] = relationship()
    condition: Mapped[PaintCondition] = relationship()
