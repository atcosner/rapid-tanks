import logging
from sqlalchemy.orm import Session

from src.components.tank import TankType
from src.constants.time import ReportingPeriodDetails
from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.tank import FixedRoofTank

from .util import ReportOutputType

logger = logging.getLogger(__name__)


class SimpleReport:
    def __init__(
            self,
            facility_id: int,
            tanks: list[tuple[TankType, int]],
            reporting_period: ReportingPeriodDetails,
    ) -> None:
        self.reporting_period = reporting_period
        self.fixed_roof_tanks = []
        self.floating_roof_tanks = []

        # Lookup the relevant tanks and facility
        with Session(DB_ENGINE, expire_on_commit=False) as session:
            self.facility = session.get(Facility, facility_id)
            for tank_type, tank_id in tanks:
                if tank_type in [TankType.HORIZONTAL_FIXED_ROOF, TankType.VERTICAL_FIXED_ROOF]:
                    self.fixed_roof_tanks.append(session.get(FixedRoofTank, tank_id))

    def calculate(self, output_type: ReportOutputType) -> None:
        # Loop through each tank and calculate the emissions
        for fixed_tank in self.fixed_roof_tanks:
            logger.info(f'Starting calculations on tank: {fixed_tank.name}')
