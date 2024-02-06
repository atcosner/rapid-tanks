from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .paint import SolarAbsorptance


class FixedRoofTank(MappedAsDataclass, OrmBase):
    __tablename__ = "fixed_roof_tank"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    facility_id = mapped_column(ForeignKey("facility.id"))
    is_vertical: Mapped[bool]

    shell_height: Mapped[str]
    shell_diameter: Mapped[str]
    shell_color_id = mapped_column(ForeignKey("paint_color.id"))
    shell_condition_id = mapped_column(ForeignKey("paint_condition.id"))

    roof_type: Mapped[str]
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

    facility: Mapped["Facility"] = relationship(init=False, back_populates="fixed_roof_tanks")
    shell_solar_absorptance: Mapped[SolarAbsorptance] = relationship(
        init=False,
        foreign_keys=[shell_color_id, shell_condition_id],
        primaryjoin="and_(FixedRoofTank.shell_color_id==SolarAbsorptance.color_id,"
                    "FixedRoofTank.shell_condition_id==SolarAbsorptance.condition_id)",
    )
    roof_solar_absorptance: Mapped[SolarAbsorptance] = relationship(
        init=False,
        foreign_keys=[roof_color_id, roof_condition_id],
        primaryjoin="and_(FixedRoofTank.roof_color_id==SolarAbsorptance.color_id,"
                    "FixedRoofTank.roof_condition_id==SolarAbsorptance.condition_id)",
    )
