from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase


class MeteorologicalSite(MappedAsDataclass, OrmBase):
    __tablename__ = "meteorological_site"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    state: Mapped[str]
    station_identifier: Mapped[str]
    gps_latitude: Mapped[str]
    gps_longitude: Mapped[str]
    atmospheric_pressure: Mapped[str]

    month_records: Mapped[list["MeteorologicalMonthRecord"]] = relationship(init=False, back_populates="site")


class MeteorologicalMonthRecord(MappedAsDataclass, OrmBase):
    __tablename__ = "meteorological_month_record"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id = mapped_column(ForeignKey("meteorological_site.id"))
    month_id: Mapped[int]
    average_temp_min: Mapped[str]
    average_temp_max: Mapped[str]
    average_wind_speed: Mapped[str]
    average_daily_insolation: Mapped[str]

    site: Mapped[MeteorologicalSite] = relationship(back_populates="month_records")
