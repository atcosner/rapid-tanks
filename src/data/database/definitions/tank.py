from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .facility import Facility


class FixedRoofType(MappedAsDataclass, OrmBase):
    __tablename__ = "fixed_roof_type"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class FixedRoofTank(MappedAsDataclass, OrmBase):
    __tablename__ = "fixed_roof_tank"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    facility_id = mapped_column(ForeignKey("facility.id"))
    is_vertical: Mapped[bool]

    shell_height: Mapped[str]
    shell_diameter: Mapped[str]
    shell_color_id = mapped_column(ForeignKey("paint_color.id"))
    shell_condition_id = mapped_column(ForeignKey("paint_condition.id"))

    roof_type_id = mapped_column(ForeignKey("fixed_roof_type.id"))
    roof_color_id = mapped_column(ForeignKey("paint_color.id"))
    roof_condition_id = mapped_column(ForeignKey("paint_condition.id"))
    roof_height: Mapped[str]
    roof_slope: Mapped[str]
    roof_radius: Mapped[str]

    vent_vacuum_setting: Mapped[str]
    vent_breather_setting: Mapped[str]

    maximum_liquid_height: Mapped[str]
    average_liquid_height: Mapped[str]
    working_volume: Mapped[str]
    turnovers_per_year: Mapped[str]
    net_throughput: Mapped[str]
    is_heated: Mapped[bool]

    facility: Mapped[Facility] = relationship(back_populates="fixed_roof_tanks")
