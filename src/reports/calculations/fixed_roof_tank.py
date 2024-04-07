import logging
from dataclasses import dataclass
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.reports.components.tanks.fixed_roof import FixedRoofTankShim
from src.reports.components.time import ReportingChunk
from src.util.logging import log_block
from src.util.errors import CalculationError
from src.util.quantities import R, PI

from ..util import TankEmission, MaterialEmission, MixtureEmission
from ...util.enums import InsulationType

logger = logging.getLogger(__name__)


@dataclass
class FixedRoofEmissions:
    facility_name: str
    tank: FixedRoofTankShim
    reporting_chunk: ReportingChunk

    # Standing loss components
    vapor_space_volume: Quantity | None = None
    stock_vapor_density: Quantity | None = None
    vapor_space_expansion_factor: Quantity | None = None

    # Working loss components
    net_working_loss_throughput: Quantity | None = None
    working_loss_turnover_factor: Quantity | None = None

    # Store intermediate reports here
    vapor_space_outage: Quantity | None = None
    average_ambient_temperature: Quantity | None = None
    average_ambient_temperature_range: Quantity | None = None
    liquid_bulk_temperature: Quantity | None = None
    average_daily_liquid_surface_temperature: Quantity | None = None
    mixture_vapor_pressure: Quantity | None = None
    mixture_molecular_weight: Quantity | None = None
    average_vapor_temperature: Quantity | None = None
    average_daily_vapor_temperature_range: Quantity | None = None
    average_daily_vapor_pressure_range: Quantity | None = None
    sum_of_increases_in_liquid_level: Quantity | None = None

    def _calculate_average_daily_ambient_temperature_range(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-11

        # Use the meteorological data from the site
        avg_max_temp__degr = self.reporting_chunk.site.average_temp_max.to('degR')
        avg_min_temp__degr = self.reporting_chunk.site.average_temp_min.to('degR')
        return unit_registry.Quantity(avg_max_temp__degr.magnitude - avg_min_temp__degr.magnitude, 'degR')

    def _calculate_liquid_bulk_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-31
        bulk_temp = (
                        self.average_ambient_temperature.to('degR').magnitude
                    )+ (
                        Decimal('0.003')
                        * self.tank.shell_solar_absorptance.coefficient
                        * self.reporting_chunk.site.average_daily_insolation
                    )

        return bulk_temp.magnitude * unit_registry.degR

    def _calculate_average_daily_liquid_surface_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-27, 1-28, and 1-29

        # This is based on which type of insulation the tank has
        if self.tank.insulation is None or self.tank.insulation.name == InsulationType.NONE:
            # Do not make assumptions and use equation 1-28, just use equation 1-27
            term1 = self.average_ambient_temperature.to('degR').magnitude \
                    * (Decimal('0.5') - (Decimal('0.8') / (Decimal('4.4') * (self.tank.shell_height / self.tank.shell_diameter) + Decimal('3.8'))))

            term2 = self.liquid_bulk_temperature.to('degR').magnitude \
                    * (Decimal('0.5') + (Decimal('0.8') / (Decimal('4.4') * (self.tank.shell_height / self.tank.shell_diameter) + Decimal('3.8'))))

            term3 = (
                        (
                            Decimal('0.021')
                            * self.tank.roof_solar_absorptance.coefficient
                            * self.reporting_chunk.site.average_daily_insolation
                        ) + (
                            Decimal('0.013')
                            * (self.tank.shell_height / self.tank.shell_diameter)
                            * self.tank.shell_solar_absorptance.coefficient
                            * self.reporting_chunk.site.average_daily_insolation
                        )
                    ) / (
                        Decimal('4.4') * (self.tank.shell_height / self.tank.shell_diameter) + Decimal('3.8')
                    )

            return (term1.magnitude + term2.magnitude + term3.magnitude) * unit_registry.degR

        elif self.tank.insulation == InsulationType.PARTIAL:
            # Equation 1-29
            return (Decimal('0.3') * self.average_ambient_temperature.to('degR')) \
                   + (
                        Decimal('0.7')
                        * self.liquid_bulk_temperature.to('degR')) \
                   + (
                        Decimal('0.005')
                        * self.tank.get_average_solar_absorption()
                        * self.reporting_chunk.site.average_daily_insolation
                      )

        elif self.tank.insulation is InsulationType.FULL:
            # Assume average liquid surface temperature equal to average liquid bulk temperature
            return self.liquid_bulk_temperature.to('degR')

        else:
            raise CalculationError(f'Unknown insulation: {self.tank.insulation}')

    def _calculate_average_vapor_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-32, 1-33, and 1-34

        # Get each variable in the correct units
        tank_size_ratio = self.tank.shell_height / self.tank.shell_diameter
        t_aa_degR = self.average_ambient_temperature.to('degR')
        t_b_degR = self.liquid_bulk_temperature.to('degR')
        alpha_r = self.tank.roof_solar_absorptance.coefficient
        alpha_s = self.tank.shell_solar_absorptance.coefficient
        solar_i = self.reporting_chunk.site.average_daily_insolation

        # This is based on which type of insulation the tank has
        if self.tank.insulation is None or self.tank.insulation.name == InsulationType.NONE:
            # Do not make assumptions and use equation 1-33, just use equation 1-32

            # T_V = (numerator_1 + numerator_2 + numerator_3 + numerator_4) / denominator

            # numerator_1 = (2.2 * (H_S / D) + 1.1) * T_AA
            numerator_1 = ((Decimal('2.2') * tank_size_ratio) + Decimal('1.1')) * t_aa_degR.magnitude

            # numerator_2 = 0.8 * T_B
            numerator_2 = Decimal('0.8') * t_b_degR.magnitude

            # numerator_3 = 0.021 * alpha_r * I
            numerator_3 = Decimal('0.021') * alpha_r * solar_i

            # numerator_4 = 0.013 * (H_S / D) * alpha_s * I
            numerator_4 = Decimal('0.013') * tank_size_ratio * alpha_s * solar_i

            # denominator = 2.2 * (H_S / D) + 1.9
            denominator = (Decimal('2.2') * tank_size_ratio) + Decimal('1.9')

            t_v = (numerator_1 + numerator_2 + numerator_3 + numerator_4) / denominator
            return unit_registry.Quantity(t_v.magnitude, 'degR')

        elif self.tank.insulation.name == InsulationType.PARTIAL:
            # Equation 1-34
            # T_V = (0.6 * T_AA) + (0.4 * T_B) + (0.01 * alpha_R * I)
            return (Decimal('0.6') * t_aa_degR) + (Decimal('0.04') * t_b_degR) + (Decimal('0.01') * alpha_r * solar_i)

        elif self.tank.insulation.name == InsulationType.FULL:
            return t_b_degR

        else:
            raise CalculationError(f'Unknown insulation: {self.tank.insulation.name}')

    def _calculate_stock_density(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-22

        # Calculate the average daily ambient temperature
        self.average_ambient_temperature = self.reporting_chunk.site.average_temp
        logger.debug(f'Average daily ambient temperature: {self.average_ambient_temperature}')

        # Calculate the liquid bulk temperature
        self.liquid_bulk_temperature = self._calculate_liquid_bulk_temperature()
        logger.debug(f'Liquid bulk temperature: {self.liquid_bulk_temperature}')

        # Calculate the average daily liquid surface temperature
        self.average_daily_liquid_surface_temperature = self._calculate_average_daily_liquid_surface_temperature()
        logger.debug(f'Average daily liquid surface temperature: {self.average_daily_liquid_surface_temperature}')

        # Calculate the mixture vapor pressure
        self.mixture_vapor_pressure = self.reporting_chunk.mixture.calculate_vapor_pressure(
            self.average_daily_liquid_surface_temperature
        )
        logger.debug(f'Mixture vapor pressure: {self.mixture_vapor_pressure}')

        # Calculate the mixture vapor molecular weight
        self.mixture_molecular_weight = self.reporting_chunk.mixture.calculate_vapor_molecular_weight(
            self.average_daily_liquid_surface_temperature
        )
        logger.debug(f'Mixture vapor molecular weight: {self.mixture_molecular_weight}')

        # Calculate the average vapor temperature
        self.average_vapor_temperature = self._calculate_average_vapor_temperature()
        logger.debug(f'Average vapor temperature: {self.average_vapor_temperature}')
        # W_V = (M_V * P_VA) / (R * T_V)
        term1 = self.mixture_molecular_weight * self.mixture_vapor_pressure
        term2 = R * self.average_vapor_temperature
        return term1 / term2

    def _calculate_average_daily_vapor_temperature_range(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-6, 1-7, and 1-7

        # Calculate the average daily ambient temperature range
        self.average_ambient_temperature_range = self._calculate_average_daily_ambient_temperature_range()
        logger.debug(f'Average ambient temperature range: {self.average_ambient_temperature_range}')

        # Get each variable in the correct units
        tank_size_ratio = self.tank.shell_height / self.tank.shell_diameter
        delta_t_aa_degR = self.average_ambient_temperature_range.to('degR')
        alpha_r = self.tank.roof_solar_absorptance.coefficient
        alpha_s = self.tank.shell_solar_absorptance.coefficient
        solar_i = self.reporting_chunk.site.average_daily_insolation

        # This is based on which type of insulation the tank has
        if self.tank.insulation is None or self.tank.insulation.name == InsulationType.NONE:
            # Do not make assumptions and use equation 1-7, just use equation 1-6

            # Term 1
            # term_1 = (1 - (0.8 / (2.2 * (H_S / D) + 1.9))) * ∆T_AA
            term_1 = Decimal(1) - Decimal('0.8') / (Decimal('2.2') * tank_size_ratio + Decimal('1.9'))
            term_1 = term_1 * delta_t_aa_degR.magnitude

            # Term 2 - Numerator
            # term_2_numerator = (0.042 * alpha_r * I) + (0.026 * (H_S / D) * alpha_s * I)
            term_2_numerator = (Decimal('0.042') * alpha_r * solar_i) + (Decimal('0.026') * tank_size_ratio * alpha_s * solar_i)

            # Term 2 - Denominator
            # term_2_denominator = 2.2 * (H_S / D) + 1.9
            term_2_denominator = Decimal('2.2') * tank_size_ratio + Decimal('1.9')

            delta_t_v = term_1 + (term_2_numerator / term_2_denominator)
            return unit_registry.Quantity(delta_t_v.magnitude, 'degR')

        elif self.tank.insulation.name == InsulationType.PARTIAL:
            # Equation 1-8
            # ∆T_V = (0.6 * ∆T_AA) + (0.02 * alpha_R * I)
            return (Decimal('0.6') * delta_t_aa_degR) + (Decimal('0.02') * alpha_r * solar_i)

        elif self.tank.insulation.name == InsulationType.FULL:
            # No variation of the vapor temperature
            return unit_registry.Quantity(Decimal(0), 'degR')

        else:
            raise CalculationError(f'Unknown insulation: {self.tank.insulation.name}')

    def _average_daily_vapor_pressure_range(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-9
        # ∆P_V = P_VX - P_VN

        # Note on Equation 1-9: Fully insulated tanks have no pressure variations due to temperature
        if self.tank.insulation.name == InsulationType.FULL:
            return Decimal('0.0') * unit_registry.psi

        # Calculate T_LX and T_LN
        t_lx__degr = self.average_daily_liquid_surface_temperature + (
                Decimal('0.25')
                * self.average_ambient_temperature_range
        )
        t_ln__degr = self.average_daily_liquid_surface_temperature - (
                Decimal('0.25')
                * self.average_ambient_temperature_range
        )

        t_lx__degf = t_lx__degr.to('degF')
        t_ln__degf = t_ln__degr.to('degF')

        # Calculate the vapor pressure at the different temperatures
        max_vapor_pressure = self.reporting_chunk.mixture.calculate_vapor_pressure(t_lx__degf)
        min_vapor_pressure = self.reporting_chunk.mixture.calculate_vapor_pressure(t_ln__degf)
        logger.debug(f'Max vapor pressure: {max_vapor_pressure}')
        logger.debug(f'Min vapor pressure: {min_vapor_pressure}')

        return max_vapor_pressure - min_vapor_pressure

    def _calculate_breather_vent_pressure_setting_range(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-10
        # ∆P_B = P_BP - P_BV

        return self.tank.vent_breather_setting - self.tank.vent_vacuum_setting

    def _calculate_vapor_space_expansion_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-5
        # K_E = ∆T_V/T_LA + (∆P_V − ∆P_B)/(P_A − P_VA)

        # Calculate the average daily vapor temperature range (∆T_V)
        self.average_daily_vapor_temperature_range = self._calculate_average_daily_vapor_temperature_range()
        logger.debug(f'Average vapor temperature range: {self.average_daily_vapor_temperature_range}')

        # Calculate the average daily vapor pressure range (∆P_V)
        self.average_daily_vapor_pressure_range = self._average_daily_vapor_pressure_range()
        logger.debug(f'Average vapor pressure range: {self.average_daily_vapor_pressure_range}')

        # Calculate the breather vent pressure (∆P_B)
        self.average_breather_pressure_range = self._calculate_breather_vent_pressure_setting_range()
        logger.debug(f'Average breather pressure range: {self.average_breather_pressure_range}')

        # Complete the equation
        # K_E = ∆T_V/T_LA + (∆P_V − ∆P_B)/(P_A − P_VA)

        term1 = self.average_daily_vapor_temperature_range / self.average_daily_liquid_surface_temperature
        term2_numerator = self.average_daily_vapor_pressure_range - self.average_breather_pressure_range
        term2_denominator = self.reporting_chunk.site.atmospheric_pressure - self.mixture_vapor_pressure

        return term1 + (term2_numerator / term2_denominator)

    def _calculate_vented_vapor_saturation_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-21
        k_s = 1 / (
                Decimal(1)
                + (Decimal('0.053')
                   * self.mixture_vapor_pressure.magnitude
                   * self.vapor_space_outage.magnitude))

        return unit_registry.Quantity(k_s, 'dimensionless')

    def _calculate_vapor_space_volume(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-3

        # Get the vapor space outage from the tank
        self.vapor_space_outage = self.tank.calculate_vapor_space_outage()
        logger.debug(f'Vapor space outage: {self.vapor_space_outage}')
        return self.tank.calculate_vapor_space_volume()

    def _calculate_standing_losses(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-2
        # L~S = 365 * V~V * W~V * K~E * K~S

        # Determine the days we are calculating losses over
        reporting_days = self.reporting_chunk.total_days()

        # Calculate the vapor space volume
        with log_block(logger.debug, 'Vapor Space Volume'):
            self.vapor_space_volume = self._calculate_vapor_space_volume()
            logger.debug(f'Vapor space volume: {self.vapor_space_volume}')

        # Calculate the stock vapor density
        with log_block(logger.debug, 'Vapor Stock Density'):
            self.stock_vapor_density = self._calculate_stock_density()
            logger.debug(f'Vapor stock density: {self.stock_vapor_density}')

        # Calculate the vapor space expansion factor
        with log_block(logger.debug, 'Vapor Space Expansion Factor'):
            self.vapor_space_expansion_factor = self._calculate_vapor_space_expansion_factor()
            logger.debug(f'Vapor space expansion factor: {self.vapor_space_expansion_factor}')

        # Calculate the vented vapor saturation factor
        with log_block(logger.debug, 'Vented Vapor Saturation Factor'):
            self.vented_vapor_saturation_factor = self._calculate_vented_vapor_saturation_factor()
            logger.debug(f'Vented vapor saturation factor: {self.vented_vapor_saturation_factor}')

        # Finish the calculation
        # L~S = <days> * V~V * W~V * K~E * K~S
        l_s = (reporting_days
               * self.vapor_space_volume.magnitude
               * self.stock_vapor_density.magnitude
               * self.vapor_space_expansion_factor.magnitude
               * self.vented_vapor_saturation_factor.magnitude)

        return l_s * unit_registry.lb / unit_registry.year

    def _calculate_sum_of_increases_in_liquid_level(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-37
        # sum(H_QI) = (5.614 * Q) / [(PI / 4) * D**2]

        # TODO: This equation is an approximation, what to do if we have the actual value

        conversion_factor = Decimal('5.614') * (unit_registry.ft**3) / unit_registry.oil_bbl
        term1 = conversion_factor * self.reporting_chunk.throughput.to('oil_bbl/year')
        term2 = (PI / 4) * self.tank.shell_diameter**2
        return term1 / term2

    def _calculate_net_working_loss_throughput(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-38
        # V_Q = sum(H_QI) * (PI / 4) * D**2

        # Ignore the approximation equation 1-39 since we handle an approximation in equation 1-37 instead
        return self.sum_of_increases_in_liquid_level * (PI / 4) * self.tank.shell_diameter**2

    def _calculate_working_loss_turnover_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-35

        # K_N = 1 (for turnovers <= 36 per year)
        if int(self.tank.turnovers_per_year) <= 36:
            return unit_registry.Quantity(Decimal(1), 'dimensionless')

        # > 36 turnovers per year uses the following equation
        # K_N = (180 + N) / (6 * N)
        # N = sum(H_QI) / (H_LX - H_LN)

        term1 = self.tank.maximum_liquid_height - self.tank.minimum_liquid_height
        n = self.sum_of_increases_in_liquid_level / term1
        k_n = (180 + n) / (6 * n)
        return unit_registry.Quantity(k_n, 'dimensionless')

    def _calculate_working_loss_product_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-35
        # This quantity lives with the material so just use one of them
        return self.reporting_chunk.mixture.components[0].material.working_loss_product_factor

    def _calculate_vent_setting_correction_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-40 and 1-41

        if (
                self.tank.vent_breather_setting > (Decimal('0.03') * unit_registry.psi)
                or self.tank.vent_vacuum_setting < (Decimal('-0.03') * unit_registry.psi)
        ):
            # Calculate Equation 1-40
            # K_N * [(P_BP + P_A) / (P_I + P_A)] > 1.0

            # TODO: P_I is the gauge pressure reading under normal conditions (0 = Tank at P_A)
            vapor_gauge_pressure = Decimal('0') * unit_registry.psi

            term1 = self.tank.vent_breather_setting + self.reporting_chunk.site.atmospheric_pressure
            term2 = vapor_gauge_pressure + self.reporting_chunk.site.atmospheric_pressure
            equation_1_40 = self.working_loss_turnover_factor * (term1 / term2)

            # Calculate Equation 1-41
            # K_B = = [((P_I + P_A) / K_N) - P_VA] / [P_BP + P_A - P_VA]
            term1 = ((vapor_gauge_pressure + self.reporting_chunk.site.atmospheric_pressure) / self.working_loss_turnover_factor) - self.mixture_vapor_pressure
            term2 = self.tank.vent_breather_setting + self.reporting_chunk.site.atmospheric_pressure - self.mixture_vapor_pressure
            equation_1_41 = term1 / term2

            # Check if Equation 1-41 should be used
            if equation_1_40 > Decimal('1.0'):
                return equation_1_41
            else:
                # TODO: What do we do if equation 1-40 is not true?
                return unit_registry.Quantity(Decimal(1), 'dimensionless')
        else:
            # If the breather vent is set between +- 0.03 psig, K_B = 1
            return unit_registry.Quantity(Decimal(1), 'dimensionless')

    def _calculate_working_losses(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-35
        # L_W = V_Q ∗ K_N ∗ K_P ∗ W_V ∗ K_B

        self.sum_of_increases_in_liquid_level = self._calculate_sum_of_increases_in_liquid_level()

        # Calculate the net working loss throughput (V_Q)
        with log_block(logger.debug, 'Net Working Loss Throughput'):
            self.net_working_loss_throughput = self._calculate_net_working_loss_throughput()
            logger.debug(f'Net Working Loss Throughput: {self.net_working_loss_throughput}')

        # Calculate the working loss turnover factor (K_N)
        with log_block(logger.debug, 'Working Loss Turnover Factor'):
            self.working_loss_turnover_factor = self._calculate_working_loss_turnover_factor()
            logger.debug(f'Working loss turnover factor: {self.working_loss_turnover_factor}')

        # Calculate the working loss product factor (K_P)
        with log_block(logger.debug, 'Working Loss Product Factor'):
            self.working_loss_product_factor = self._calculate_working_loss_product_factor()
            logger.debug(f'Working loss product factor: {self.working_loss_product_factor}')

        # Calculate the vent setting correction factor (K_B)
        with log_block(logger.debug, 'Vent Setting Correction Factor'):
            self.vent_setting_correction_factor = self._calculate_vent_setting_correction_factor()
            logger.debug(f'Vent setting correction factor: {self.vent_setting_correction_factor}')

        # Finish the calculation
        # L_W = V_Q ∗ K_N ∗ K_P ∗ W_V ∗ K_B
        l_w = (self.net_working_loss_throughput.magnitude
               * self.working_loss_turnover_factor.magnitude
               * self.working_loss_product_factor.magnitude
               * self.stock_vapor_density.magnitude
               * self.vent_setting_correction_factor.magnitude)

        return l_w * unit_registry.lb / unit_registry.year

    def calculate_total_emissions(self) -> TankEmission:
        # Calculate standing losses
        if self.tank.is_underground and not self.tank.is_vertical:
            # No standing losses for underground vertical tanks (7.1-21, Note on 1-15)
            standing_losses = Decimal(0) * unit_registry.lb
        else:
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
