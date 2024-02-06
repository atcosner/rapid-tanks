from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.meteorological import MeteorologicalSite


with Session(DB_ENGINE) as session:
    for facility in session.scalars(select(Facility)).all():
        print(facility)

    for site in session.scalars(select(MeteorologicalSite)).all():
        print(site)
