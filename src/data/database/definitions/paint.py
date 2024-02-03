from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass

from . import OrmBase


class PaintColor(MappedAsDataclass, OrmBase):
    __tablename__ = "paint_color"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class PaintCondition(MappedAsDataclass, OrmBase):
    __tablename__ = "paint_condition"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
