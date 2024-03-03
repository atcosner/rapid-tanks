from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship

from . import OrmBase
from .mixture import PetrochemicalMixture
from .util import PintQuantity


class ServiceRecord(MappedAsDataclass, OrmBase):
    __tablename__ = "service_record"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    tank_id = mapped_column(ForeignKey("fixed_roof_tank.id"))
    mixture_id = mapped_column(ForeignKey("petrochemical_mixture.id"))

    start_date: Mapped[date]
    end_date: Mapped[date]
    throughput: Mapped[PintQuantity] = mapped_column(PintQuantity('gal/yr'))

    tank: Mapped["FixedRoofTank"] = relationship(init=False, back_populates="service_records")
    mixture: Mapped[PetrochemicalMixture] = relationship(init=False)
