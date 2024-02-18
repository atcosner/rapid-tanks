from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .paint import SolarAbsorptance


class FixedRoofTank(MappedAsDataclass, OrmBase):
    __tablename__ = "fixed_roof_tank"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default='')
    facility_id = mapped_column(ForeignKey("facility.id"))
    is_vertical: Mapped[bool] = mapped_column(default=True)

    shell_height: Mapped[str] = mapped_column(default='0.0')
    shell_diameter: Mapped[str] = mapped_column(default='0.0')
    shell_color_id = mapped_column(ForeignKey("paint_color.id"))
    shell_condition_id = mapped_column(ForeignKey("paint_condition.id"))

    roof_type: Mapped[str] = mapped_column(default='')
    roof_color_id = mapped_column(ForeignKey("paint_color.id"))
    roof_condition_id = mapped_column(ForeignKey("paint_condition.id"))
    roof_height: Mapped[str] = mapped_column(default='0.0')
    roof_slope: Mapped[str] = mapped_column(default='0.0625')
    roof_radius: Mapped[str] = mapped_column(default='0.0')

    vent_vacuum_setting: Mapped[str] = mapped_column(default='-0.3')
    vent_breather_setting: Mapped[str] = mapped_column(default='0.3')

    maximum_liquid_height: Mapped[str] = mapped_column(default='0.0')
    average_liquid_height: Mapped[str] = mapped_column(default='0.0')
    working_volume: Mapped[str] = mapped_column(default='0.0')
    turnovers_per_year: Mapped[str] = mapped_column(default='0')
    net_throughput: Mapped[str] = mapped_column(default='0.0')
    is_heated: Mapped[bool] = mapped_column(default=False)

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
