from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass

from . import OrmBase
from .fittings import IfrtFittingAssociation
from .paint import PaintColor, PaintCondition, SolarAbsorptance
from .seals import SealSecondaryType
from .util import PintQuantity


class InternalFloatingRoofTank(MappedAsDataclass, OrmBase):
    __tablename__ = "internal_floating_roof_tank"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column()

    # Properties
    shell_height: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'))
    shell_diameter: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'))

    support_column_count: Mapped[int]

    # Relationships
    facility_id = mapped_column(ForeignKey("facility.id"))
    facility: Mapped["Facility"] = relationship(init=False, back_populates="internal_floating_roof_tanks")

    shell_paint_color_id = mapped_column(ForeignKey("paint_color.id"))
    shell_paint_color: Mapped[PaintColor] = relationship(init=False, foreign_keys=shell_paint_color_id)

    shell_paint_condition_id = mapped_column(ForeignKey("paint_condition.id"))
    shell_paint_condition: Mapped[PaintCondition] = relationship(init=False, foreign_keys=shell_paint_condition_id)

    shell_solar_absorptance: Mapped[SolarAbsorptance] = relationship(
        init=False,
        foreign_keys=[shell_paint_color_id, shell_paint_condition_id],
        primaryjoin="and_(InternalFloatingRoofTank.shell_paint_color_id==SolarAbsorptance.color_id,"
                    "InternalFloatingRoofTank.shell_paint_condition_id==SolarAbsorptance.condition_id)",
        viewonly=True,
    )

    roof_paint_color_id = mapped_column(ForeignKey("paint_color.id"))
    roof_paint_color: Mapped[PaintColor] = relationship(init=False, foreign_keys=roof_paint_color_id)

    roof_paint_condition_id = mapped_column(ForeignKey("paint_condition.id"))
    roof_paint_condition: Mapped[PaintCondition] = relationship(init=False, foreign_keys=roof_paint_condition_id)

    roof_solar_absorptance: Mapped[SolarAbsorptance] = relationship(
        init=False,
        foreign_keys=[roof_paint_color_id, roof_paint_condition_id],
        primaryjoin="and_(InternalFloatingRoofTank.roof_paint_color_id==SolarAbsorptance.color_id,"
                    "InternalFloatingRoofTank.roof_paint_condition_id==SolarAbsorptance.condition_id)",
        viewonly=True,
    )

    seal_id = mapped_column(ForeignKey("seal_secondary_type.id"))
    seal: Mapped[SealSecondaryType] = relationship(init=False, viewonly=True)

    fittings: Mapped[list[IfrtFittingAssociation]] = relationship(init=False, viewonly=True)
