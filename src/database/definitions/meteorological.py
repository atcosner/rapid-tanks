from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship
from sqlalchemy.orm.collections import attribute_keyed_dict

from . import OrmBase
from .util import PintQuantity


class MeteorologicalSite(MappedAsDataclass, OrmBase):
    __tablename__ = "meteorological_site"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    state: Mapped[str]
    station_identifier: Mapped[str]
    gps_latitude: Mapped[str]
    gps_longitude: Mapped[str]
    atmospheric_pressure: Mapped[PintQuantity] = mapped_column(PintQuantity('psia'))

    month_records: Mapped[dict[int, "MeteorologicalMonthRecord"]] = relationship(
        collection_class=attribute_keyed_dict("month_id"),
        back_populates="site",
    )


class MeteorologicalMonthRecord(MappedAsDataclass, OrmBase):
    __tablename__ = "meteorological_month_record"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    site_id = mapped_column(ForeignKey("meteorological_site.id"))
    month_id: Mapped[int]
    average_temp_min: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'))
    average_temp_max: Mapped[PintQuantity] = mapped_column(PintQuantity('degF'))
    average_wind_speed: Mapped[PintQuantity] = mapped_column(PintQuantity('mi/hr'))
    average_daily_insolation: Mapped[PintQuantity] = mapped_column(PintQuantity('dimensionless'))  # btu/(ft^2 day)

    site: Mapped[MeteorologicalSite] = relationship(init=False, back_populates="month_records")
