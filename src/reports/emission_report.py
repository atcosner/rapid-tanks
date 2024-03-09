import logging
from sqlalchemy.orm import Session

from src.components.tank import FixedRoofTankShim
from ..util.enums import TankType
from src.constants.meteorological import MeteorologicalSiteShim
from src.constants.time import ReportingPeriod
from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.tank import FixedRoofTank

from .calculations.fixed_roof import FixedRoofEmissions
from .util import ReportOutputType

logger = logging.getLogger(__name__)


class EmissionReport:
    def __init__(
            self,
            facility_id: int,
            tanks: list[tuple[TankType, int]],
            reporting_period: ReportingPeriod,
    ) -> None:
        self.reporting_period = reporting_period
        self.fixed_roof_tanks = []
        self.floating_roof_tanks = []

        # Lookup the relevant tanks and facility
        self.session = Session(DB_ENGINE)
        self.facility = self.session.get(Facility, facility_id)
        assert self.facility is not None, f'No facility with id: {facility_id}'

        for tank_type, tank_id in tanks:
            if tank_type in [TankType.HORIZONTAL_FIXED_ROOF, TankType.VERTICAL_FIXED_ROOF]:
                tank = self.session.get(FixedRoofTank, tank_id)
                assert tank is not None, f'No tank with id: {tank_id}'
                self.fixed_roof_tanks.append(tank)

    def calculate(self, output_type: ReportOutputType) -> None:
        all_emissions = []

        # Break up the reporting period into smaller partitions
        for report_chunk in self.reporting_period.get_chunks():
            # Loop through each tank and calculate the emissions
            for fixed_tank in self.fixed_roof_tanks:
                logger.info(f'Starting calculations on tank: {fixed_tank.name}')
                tank_emissions = FixedRoofEmissions(
                    facility_name=self.facility.name,
                    site=MeteorologicalSiteShim(self.facility.site),
                    tank=FixedRoofTankShim(fixed_tank),
                    reporting_chunk=report_chunk,
                )
                all_emissions.append(tank_emissions.calculate_total_emissions())

            # Report on all the emissions we calculated
            if output_type is ReportOutputType.LOG:
                pass

        self.session.close()
