import logging
from decimal import Decimal
from pint import Quantity

from src import unit_registry
from src.components.fixed_roof_tank import FixedRoofTank
from src.components.site import Site
from src.components.tank import Insulation
from src.util.logging import log_block
from src.util.errors import CalculationError

logger = logging.getLogger(__name__)


class FixedRoofLosses:
    def __init__(self, site: Site, tank: FixedRoofTank) -> None:
        self.site = site
        self.tank = tank

        self.total_losses: Quantity | None = None

        # Standing loss components
        self.vapor_space_volume: Quantity | None = None
        self.stock_vapor_density: Quantity | None = None
        self.vapor_space_expansion_factor: Quantity | None = None

        # Working loss components
        self.net_working_loss_throughput: Quantity | None = None
        self.working_loss_turnover_factor: Quantity | None = None

        # Store intermediate calculations here
        self.vapor_space_outage: Quantity | None = None
        self.average_ambient_temperature: Quantity | None = None
        self.average_ambient_temperature_range: Quantity | None = None
        self.liquid_bulk_temperature: Quantity | None = None
        self.average_daily_liquid_surface_temperature: Quantity | None = None
        self.mixture_vapor_pressure: Quantity | None = None
        self.mixture_molecular_weight: Quantity | None = None
        self.average_vapor_temperature: Quantity | None = None
        self.average_daily_vapor_temperature_range: Quantity | None = None
        self.average_daily_vapor_pressure_range: Quantity | None = None

    def _calculate_average_daily_ambient_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-30

        # Use the meteorological data from the site
        # TODO: This needs to be adjusted for the time period we are calculating over
        avg_max_temp_degR = self.site.meteorological_data.average_daily_max_temp.to('degR')
        avg_min_temp_degR = self.site.meteorological_data.average_daily_min_temp.to('degR')

        return (avg_max_temp_degR + avg_min_temp_degR) / 2

    def _calculate_average_daily_ambient_temperature_range(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-11

        # Use the meteorological data from the site
        # TODO: This needs to be adjusted for the time period we are calculating over
        avg_max_temp_degR = self.site.meteorological_data.average_daily_max_temp.to('degR')
        avg_min_temp_degR = self.site.meteorological_data.average_daily_min_temp.to('degR')
        return avg_max_temp_degR - avg_min_temp_degR

    def _calculate_liquid_bulk_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-31
        bulk_temp = self.average_ambient_temperature.to('degR').magnitude \
                    + (Decimal('0.003')
                       * self.tank.shell_solar_absorption
                       * self.site.meteorological_data.solar_insolation)

        return bulk_temp.magnitude * unit_registry.degR

    def _calculate_average_daily_liquid_surface_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-27, 1-28, and 1-29

        # This is based on which type of insulation the tank has
        if self.tank.insulation is Insulation.NONE:
            # Do not make assumptions and use equation 1-28, just use equation 1-27
            term1 = self.average_ambient_temperature.to('degR').magnitude \
                    * (Decimal('0.5') - (Decimal('0.8') / (Decimal('4.4') * (self.tank.height / self.tank.diameter) + Decimal('3.8'))))

            term2 = self.liquid_bulk_temperature.to('degR').magnitude \
                    * (Decimal('0.5') + (Decimal('0.8') / (Decimal('4.4') * (self.tank.height / self.tank.diameter) + Decimal('3.8'))))

            term3 = (
                        (Decimal('0.021') * self.tank.roof_solar_absorption * self.site.meteorological_data.solar_insolation)
                        + (Decimal('0.013') * (self.tank.height / self.tank.diameter) * self.tank.shell_solar_absorption * self.site.meteorological_data.solar_insolation)
                    ) / (
                        Decimal('4.4') * (self.tank.height / self.tank.diameter) + Decimal('3.8')
                    )

            return (term1.magnitude + term2.magnitude + term3.magnitude) * unit_registry.degR

        elif self.tank.insulation is Insulation.PARTIAL:
            # Equation 1-28
            return (Decimal('0.4') * self.average_ambient_temperature.to('degR')) \
                   + (Decimal('0.06') * self.liquid_bulk_temperature.to('degR')) \
                   + (Decimal('0.005')
                      * self.tank.get_average_solar_absorption()
                      * self.site.meteorological_data.solar_insolation)

        elif self.tank.insulation is Insulation.FULL:
            # Equation 1-29
            return self.liquid_bulk_temperature.to('degR')

        else:
            # What?
            raise CalculationError(f'Unknown insulation: {self.tank.insulation}')

    def _calculate_average_vapor_temperature(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-32, 1-33, and 1-34

        # Get each variable in the correct units
        tank_size_ratio = self.tank.height / self.tank.diameter
        t_aa_degR = self.average_ambient_temperature.to('degR')
        t_b_degR = self.liquid_bulk_temperature.to('degR')
        alpha_r = self.tank.roof_solar_absorption
        alpha_s = self.tank.shell_solar_absorption
        solar_i = self.site.meteorological_data.solar_insolation

        # This is based on which type of insulation the tank has
        if self.tank.insulation is Insulation.NONE:
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

        elif self.tank.insulation is Insulation.PARTIAL:
            # Equation 1-34
            # T_V = (0.6 * T_AA) + (0.4 * T_B) + (0.01 * alpha_R * I)
            return (Decimal('0.6') * t_aa_degR) + (Decimal('0.04') * t_b_degR) + (Decimal('0.01') * alpha_r * solar_i)

        elif self.tank.insulation is Insulation.FULL:
            return t_b_degR

        else:
            # What?
            raise CalculationError(f'Unknown insulation: {self.tank.insulation}')

    def _calculate_stock_density(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-22

        # Calculate the average daily ambient temperature
        self.average_ambient_temperature = self._calculate_average_daily_ambient_temperature()
        logger.debug(f'Average daily ambient temperature: {self.average_ambient_temperature}')

        # Calculate the liquid bulk temperature
        self.liquid_bulk_temperature = self._calculate_liquid_bulk_temperature()
        logger.debug(f'Liquid bulk temperature: {self.liquid_bulk_temperature}')

        # Calculate the average daily liquid surface temperature
        self.average_daily_liquid_surface_temperature = self._calculate_average_daily_liquid_surface_temperature()
        logger.debug(f'Average daily liquid surface temperature: {self.average_daily_liquid_surface_temperature}')

        # Calculate the mixture vapor pressure
        self.mixture_vapor_pressure = self.tank.mixture.calculate_vapor_pressure(self.average_daily_liquid_surface_temperature)
        logger.debug(f'Mixture vapor pressure: {self.mixture_vapor_pressure}')

        # Calculate the mixture vapor molecular weight
        self.mixture_molecular_weight = self.tank.mixture.calculate_vapor_molecular_weight(self.average_daily_liquid_surface_temperature)
        logger.debug(f'Mixture vapor molecular weight: {self.mixture_molecular_weight}')

        # Calculate the average vapor temperature
        self.average_vapor_temperature = self._calculate_average_vapor_temperature()
        logger.debug(f'Average vapor temperature: {self.average_vapor_temperature}')

        # W_V = (M_V * P_VA) / (R * T_V)
        term1 = self.mixture_molecular_weight.magnitude * self.mixture_vapor_pressure.magnitude
        term2 = Decimal('10.731') * self.average_vapor_temperature.magnitude
        return unit_registry.Quantity(term1 / term2, 'dimensionless')

    def _calculate_average_daily_vapor_temperature_range(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-6, 1-7, and 1-7

        # Calculate the average daily ambient temperature range
        self.average_ambient_temperature_range = self._calculate_average_daily_ambient_temperature_range()
        logger.debug(f'Average ambient temperature range: {self.average_ambient_temperature_range}')

        # Get each variable in the correct units
        tank_size_ratio = self.tank.height / self.tank.diameter
        delta_t_aa_degR = self.average_ambient_temperature_range.to('degR')
        alpha_r = self.tank.roof_solar_absorption
        alpha_s = self.tank.shell_solar_absorption
        solar_i = self.site.meteorological_data.solar_insolation

        # This is based on which type of insulation the tank has
        if self.tank.insulation is Insulation.NONE:
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

        elif self.tank.insulation is Insulation.PARTIAL:
            # Equation 1-8
            # ∆T_V = (0.6 * ∆T_AA) + (0.02 * alpha_R * I)
            return (Decimal('0.6') * delta_t_aa_degR) + (Decimal('0.02') * alpha_r * solar_i)

        elif self.tank.insulation is Insulation.FULL:
            # No variation of the vapor temperature
            return unit_registry.Quantity(Decimal(0), 'degR')

        else:
            # What?
            raise CalculationError(f'Unknown insulation: {self.tank.insulation}')

    def _average_daily_vapor_pressure_range(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-9
        # ∆P_V = P_VX - P_VN

        # Calculate T_LX and T_LN
        t_lx_degR = self.average_daily_liquid_surface_temperature + (Decimal('0.25') * self.average_ambient_temperature_range)
        t_ln_degR = self.average_daily_liquid_surface_temperature - (Decimal('0.25') * self.average_ambient_temperature_range)

        t_lx_degF = t_lx_degR.to('degF')
        t_ln_degF = t_ln_degR.to('degF')

        # Calculate the vapor pressure at the different temperatures
        max_vapor_pressure = self.tank.mixture.calculate_vapor_pressure(t_lx_degF)
        min_vapor_pressure = self.tank.mixture.calculate_vapor_pressure(t_ln_degF)
        logger.debug(f'Max vapor pressure: {max_vapor_pressure}')
        logger.debug(f'Min vapor pressure: {min_vapor_pressure}')

        return max_vapor_pressure - min_vapor_pressure

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
        # TODO: Actually calculate this
        self.average_breather_pressure_range = unit_registry.Quantity(Decimal('0.06'), 'psia')
        logger.debug(f'Average breather pressure range: {self.average_breather_pressure_range}')

        # Complete the equation
        # K_E = ∆T_V/T_LA + (∆P_V − ∆P_B)/(P_A − P_VA)

        term1 = self.average_daily_vapor_temperature_range / self.average_daily_liquid_surface_temperature
        term2_numerator = self.average_daily_vapor_pressure_range - self.average_breather_pressure_range
        term2_denominator = self.site.meteorological_data.atmospheric_pressure - self.mixture_vapor_pressure

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

        # Get the vapor space volume from the tank
        return self.tank.calculate_vapor_space_volume()

    def _calculate_standing_losses(self) -> Quantity:
        logger.info(f'Calculating standing losses for "{self.tank.name}" at "{self.site.name}"')

        # AP 42 Chapter 7 Equation 1-2
        # L~S = 365 * V~V * W~V * K~E * K~S

        # Determine the days we are calculating losses over
        days = 365  # TODO: Actually do this

        # Calculate the vapor space volume
        with log_block(logger, 'Vapor Space Volume'):
            self.vapor_space_volume = self._calculate_vapor_space_volume()
            logger.info(f'Vapor space volume: {self.vapor_space_volume}')

        # Calculate the stock vapor density
        with log_block(logger, 'Vapor Stock Density'):
            self.stock_vapor_density = self._calculate_stock_density()
            logger.info(f'Vapor stock density: {self.stock_vapor_density}')

        # Calculate the vapor space expansion factor
        with log_block(logger, 'Vapor Space Expansion Factor'):
            self.vapor_space_expansion_factor = self._calculate_vapor_space_expansion_factor()
            logger.info(f'Vapor space expansion factor: {self.vapor_space_expansion_factor}')

        # Calculate the vented vapor saturation factor
        with log_block(logger, 'Vented Vapor Saturation Factor'):
            self.vented_vapor_saturation_factor = self._calculate_vented_vapor_saturation_factor()
            logger.info(f'Vented vapor saturation factor: {self.vented_vapor_saturation_factor}')

        # Finish the calculation
        # L~S = 365 * V~V * W~V * K~E * K~S
        l_s = (days
               * self.vapor_space_volume.magnitude
               * self.stock_vapor_density.magnitude
               * self.vapor_space_expansion_factor.magnitude
               * self.vented_vapor_saturation_factor.magnitude)

        return l_s * unit_registry.lb / unit_registry.year

    def _calculate_net_working_loss_throughput(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-38

        # TODO: Handle if we know the net increase in liquid level

        # Use Equation 1-39 to estimate this from tank throughput if we dont
        # TODO: This needs to be aware of the date range we are calculating emissions for
        conversion_factor = Decimal('5.614') * (unit_registry.ft**3) / unit_registry.oil_bbl
        return conversion_factor * self.tank.throughput.to('oil_bbl/year')

    def _calculate_working_loss_turnover_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-38

        # TODO: Handle > 36 turnovers in the date range
        # For turnovers <= 36, this is 1
        return unit_registry.Quantity(Decimal(1), 'dimensionless')

    def _calculate_working_loss_product_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-35
        # This quantity lives with the material so just use one of them
        return self.tank.mixture.parts[0].material.working_loss_product_factor

    def _calculate_vent_setting_correction_factor(self) -> Quantity:
        # AP 42 Chapter 7 Equation 1-40 and 1-41

        # TODO: Calculate this using the equation for non-standard breather vent settings

        # If the breather vent is set between +- 0.03 psig, K_B = 1
        return unit_registry.Quantity(Decimal(1), 'dimensionless')

    def _calculate_working_losses(self) -> Quantity:
        logger.info(f'Calculating working losses for "{self.tank.name}" at "{self.site.name}"')

        # AP 42 Chapter 7 Equation 1-35
        # L_W = V_Q ∗ K_N ∗ K_P ∗ W_V ∗ K_B

        # Calculate the net working loss throughput (V_Q)
        with log_block(logger, 'Net Working Loss Throughput'):
            self.net_working_loss_throughput = self._calculate_net_working_loss_throughput()
            logger.info(f'Net Working Loss Throughput: {self.net_working_loss_throughput}')

        # Calculate the working loss turnover factor (K_N)
        with log_block(logger, 'Working Loss Turnover Factor'):
            self.working_loss_turnover_factor = self._calculate_working_loss_turnover_factor()
            logger.info(f'Working loss turnover factor: {self.working_loss_turnover_factor}')

        # Calculate the working loss product factor (K_P)
        with log_block(logger, 'Working Loss Product Factor'):
            self.working_loss_product_factor = self._calculate_working_loss_product_factor()
            logger.info(f'Working loss product factor: {self.working_loss_product_factor}')

        # Calculate the vent setting correction factor (K_B)
        with log_block(logger, 'Vent Setting Correction Factor'):
            self.vent_setting_correction_factor = self._calculate_vent_setting_correction_factor()
            logger.info(f'Vent setting correction factor: {self.vent_setting_correction_factor}')

        # Finish the calculation
        # L_W = V_Q ∗ K_N ∗ K_P ∗ W_V ∗ K_B
        l_w = (self.net_working_loss_throughput.magnitude
               * self.working_loss_turnover_factor.magnitude
               * self.working_loss_product_factor.magnitude
               * self.stock_vapor_density.magnitude
               * self.vent_setting_correction_factor.magnitude)

        return l_w * unit_registry.lb / unit_registry.year

    def calculate_total_losses(self) -> dict[str, Quantity]:
        logger.info(f'Calculating total losses for "{self.tank.name}" at "{self.site.name}"')

        # Calculate standing losses
        standing_losses = self._calculate_standing_losses()
        logger.info(f'Standing losses: {standing_losses}')

        # Calculate working losses
        working_losses = self._calculate_working_losses()
        logger.info(f'Working losses: {working_losses}')

        # AP 42 Chapter 7 Equation 1-1
        # L_T = L_S + L_W
        self.total_losses = standing_losses + working_losses
        logger.info(f'Total losses: {self.total_losses}')

        # Calculate the emissions per part of the mixture
        return {part.material.name: part.weight_fraction * self.total_losses for part in self.tank.mixture.parts}
