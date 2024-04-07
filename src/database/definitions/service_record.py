from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .mixture import Mixture
from .util import PintQuantity


class FrtServiceRecord(MappedAsDataclass, OrmBase):
    __tablename__ = "frt_service_record"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    tank_id = mapped_column(ForeignKey("fixed_roof_tank.id"))
    mixture_id = mapped_column(ForeignKey("mixture.id"))

    start_date: Mapped[date]
    end_date: Mapped[date]
    throughput: Mapped[PintQuantity] = mapped_column(PintQuantity('gal/yr'))

    tank: Mapped["FixedRoofTank"] = relationship(init=False, back_populates="service_records")
    mixture: Mapped[Mixture] = relationship(init=False)


class IfrtServiceRecord(MappedAsDataclass, OrmBase):
    __tablename__ = "ifrt_service_record"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    tank_id = mapped_column(ForeignKey("internal_floating_roof_tank.id"))
    mixture_id = mapped_column(ForeignKey("mixture.id"))

    start_date: Mapped[date]
    end_date: Mapped[date]
    sum_liquid_level_decrease: Mapped[PintQuantity] = mapped_column(PintQuantity('ft/yr'), nullable=True)
    throughput: Mapped[PintQuantity] = mapped_column(PintQuantity('gal/yr'), nullable=True)

    tank: Mapped["InternalFloatingRoofTank"] = relationship(init=False, back_populates="service_records")
    mixture: Mapped[Mixture] = relationship(init=False)
