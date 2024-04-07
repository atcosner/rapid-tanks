import logging
from dataclasses import dataclass

from src.reports.components.tanks.internal_floating_roof import InternalFloatingRoofTankShim
from src.reports.components.time import ReportingChunk
from src.reports.util import TankEmission, MixtureEmission, MaterialEmission

logger = logging.getLogger(__name__)


@dataclass
class InternalFloatingRoofEmissions:
    facility_name: str
    tank: InternalFloatingRoofTankShim
    reporting_chunk: ReportingChunk

    def calculate_total_emissions(self) -> TankEmission:
        # Calculate standing losses
        standing_losses = self._calculate_standing_losses()
        logger.info(f'Standing losses: {standing_losses}')

        # Calculate working losses
        working_losses = self._calculate_working_losses()
        logger.info(f'Working losses: {working_losses}')

        # AP 42 Chapter 7 Equation 1-1
        # L_T = L_S + L_W
        total_losses = standing_losses + working_losses
        logger.info(f'Total losses: {total_losses}')

        # Calculate the emissions per part of the mixture
        standing_emissions = []
        working_emissions = []
        for component in self.reporting_chunk.mixture.components:
            standing_emissions.append(
                MaterialEmission(
                    material_id=component.material.id,
                    material_name=component.material.name,
                    emissions=component.vapor_weight_fraction * standing_losses,
                )
            )
            working_emissions.append(
                MaterialEmission(
                    material_id=component.material.id,
                    material_name=component.material.name,
                    emissions=component.vapor_weight_fraction * working_losses,
                )
            )

        return TankEmission(
            tank_id=self.tank.id,
            tank_name=self.tank.name,
            standing_losses=MixtureEmission(
                mixture_id=self.reporting_chunk.mixture.db_id,
                mixture_name=self.reporting_chunk.mixture.name,
                material_emissions=standing_emissions,
            ),
            working_losses=MixtureEmission(
                mixture_id=self.reporting_chunk.mixture.db_id,
                mixture_name=self.reporting_chunk.mixture.name,
                material_emissions=working_emissions,
            ),
        )
