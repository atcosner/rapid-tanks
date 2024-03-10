import logging
from sqlalchemy.orm import Session

from src.reports.components.tank import FixedRoofTankShim
from src.reports.components.time import ReportingPeriod, ReportingChunk
from src.database import DB_ENGINE
from src.database.definitions.facility import Facility
from src.database.definitions.tank import FixedRoofTank

from .calculations.fixed_roof import FixedRoofEmissions
from .components.meteorological import MeteorologicalChunk
from .components.mixture import MixtureShim
from .util import ReportOutputType
from ..util.enums import TankType

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

    def build_reporting_chunks(self, tank: FixedRoofTank) -> list[ReportingChunk]:
        report_start, report_end = self.reporting_period.get_date_range()
        chunks = []

        # Determine all the tank service records that overlap with our reporting range
        for record in tank.service_records:
            if (report_start <= record.end_date) and (record.start_date <= report_end):
                # Start at the latter of the range starting or the record starting
                chunk_start = max(report_start, record.start_date)
                chunk_end = min(report_end, record.end_date)

                # Adjust the throughput to match the chunk
                throughput_per_day = record.throughput / (record.end_date - record.start_date).days
                chunk_throughput = throughput_per_day * (chunk_end - chunk_start).days

                chunks.append(
                    ReportingChunk(
                        start_date=chunk_start,
                        end_date=chunk_end,
                        mixture=MixtureShim.from_mixture(record.mixture),
                        throughput=chunk_throughput,
                        site=MeteorologicalChunk.from_site(self.facility.site, chunk_start, chunk_end),
                    )
                )

        return chunks

    def calculate(self, output_type: ReportOutputType) -> None:
        all_emissions = []

        # Loop through each tank and calculate the emissions
        for fixed_tank in self.fixed_roof_tanks:
            logger.info(f'{self.facility.name}: Tank {fixed_tank.name}')
            for chunk in self.build_reporting_chunks(fixed_tank):
                logger.info(f'chunk; start: {chunk.start_date}, end: {chunk.end_date}, mixture: {chunk.mixture.name}')

                tank_emissions = FixedRoofEmissions(
                    facility_name=self.facility.name,
                    tank=FixedRoofTankShim(fixed_tank),
                    reporting_chunk=chunk,
                )
                all_emissions.append(tank_emissions.calculate_total_emissions())

        # Total the emissions per material
        emissions_per_material = {}
        for tank_emissions in all_emissions:
            for material_emissions in tank_emissions.material_emissions:
                key = (material_emissions.material_id, material_emissions.material_name)
                if key in emissions_per_material:
                    emissions_per_material[key] += material_emissions.emissions
                else:
                    emissions_per_material[key] = material_emissions.emissions

        for (_, name), emissions in emissions_per_material.items():
            logger.info(f'{name}: {emissions}')

        self.session.close()
