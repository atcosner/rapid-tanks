import logging
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedAsDataclass

from . import OrmBase
from .paint import PaintColor, PaintCondition, SolarAbsorptance
from .service_record import ServiceRecord
from .util import PintQuantity

logger = logging.getLogger(__name__)


class FixedRoofType(MappedAsDataclass, OrmBase):
    __tablename__ = "fixed_roof_type"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]


class FixedRoofTank(MappedAsDataclass, OrmBase):
    __tablename__ = "fixed_roof_tank"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(default='')
    facility_id = mapped_column(ForeignKey("facility.id"))
    is_vertical: Mapped[bool] = mapped_column(default=True)

    shell_height: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'), default='0.0')
    shell_diameter: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'), default='0.0')
    shell_color_id = mapped_column(ForeignKey("paint_color.id"))
    shell_condition_id = mapped_column(ForeignKey("paint_condition.id"))

    roof_type_id = mapped_column(ForeignKey("fixed_roof_type.id"))
    roof_color_id = mapped_column(ForeignKey("paint_color.id"))
    roof_condition_id = mapped_column(ForeignKey("paint_condition.id"))
    roof_height: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'), default='0.0')
    roof_slope: Mapped[PintQuantity] = mapped_column(PintQuantity('ft/ft'), default='0.0625')
    roof_radius: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'), default='0.0')

    vent_vacuum_setting: Mapped[PintQuantity] = mapped_column(PintQuantity('psi'), default='-0.03')  # Gauge PSI
    vent_breather_setting: Mapped[PintQuantity] = mapped_column(PintQuantity('psi'), default='0.03')  # Gauge PSI

    maximum_liquid_height: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'), default='0.0')
    average_liquid_height: Mapped[PintQuantity] = mapped_column(PintQuantity('ft'), default='0.0')
    working_volume: Mapped[PintQuantity] = mapped_column(PintQuantity('gal'), default='0.0')
    turnovers_per_year: Mapped[str] = mapped_column(default='0')
    net_throughput: Mapped[PintQuantity] = mapped_column(PintQuantity('gal/yr'), default='0.0')
    is_heated: Mapped[bool] = mapped_column(default=False)

    # Relationships

    facility: Mapped["Facility"] = relationship(init=False, back_populates="fixed_roof_tanks")
    roof_type: Mapped[FixedRoofType] = relationship(init=False)

    shell_paint_color: Mapped[PaintColor] = relationship(init=False, foreign_keys=shell_color_id)
    shell_paint_condition: Mapped[PaintCondition] = relationship(init=False, foreign_keys=shell_condition_id)
    shell_solar_absorptance: Mapped[SolarAbsorptance] = relationship(
        init=False,
        foreign_keys=[shell_color_id, shell_condition_id],
        primaryjoin="and_(FixedRoofTank.shell_color_id==SolarAbsorptance.color_id,"
                    "FixedRoofTank.shell_condition_id==SolarAbsorptance.condition_id)",
        viewonly=True,
    )

    roof_paint_color: Mapped[PaintColor] = relationship(init=False, foreign_keys=roof_color_id)
    roof_paint_condition: Mapped[PaintCondition] = relationship(init=False, foreign_keys=roof_condition_id)
    roof_solar_absorptance: Mapped[SolarAbsorptance] = relationship(
        init=False,
        foreign_keys=[roof_color_id, roof_condition_id],
        primaryjoin="and_(FixedRoofTank.roof_color_id==SolarAbsorptance.color_id,"
                    "FixedRoofTank.roof_condition_id==SolarAbsorptance.condition_id)",
        viewonly=True,
    )

    service_records: Mapped[list[ServiceRecord]] = relationship(init=False, back_populates="tank", cascade="all, delete-orphan")
