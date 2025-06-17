from .durometer import get_strain_from_stress

class MethodABearing:
    """
    Represents a Method A designed elastomeric bearing pad used in structural applications.

    The MethodABearing class is utilized to evaluate the compliance of an elastomeric bearing pad
    structured to Method A design checks. The assessment involves evaluating critical parameters
    such as internal and external layer thickness, shape factors, and edge cover, based on defined
    design specifications. Various checks are performed to ensure the pad satisfies these structural
    criteria.

    Attributes:
        width (float): The width of the bearing pad in inches.
        length (float): The length of the bearing pad in inches.
        height (float): The overall height of the bearing pad in inches.
        durometer (float): The durometer hardness value of the elastomeric material.
        internal_t (float): The thickness of the internal elastomeric layers in inches.
        external_t (float): The thickness of the external elastomeric layers in inches.
        steel_t (float): The thickness of the steel reinforcing shims in inches.
        plys (int): The number of steel layers in the bearing pad.
        edge_cover (float): The edge cover dimension in inches, default is 0.25 inches.
        checks (dict): A dictionary storing the results of various design validation checks.
        internal_shape_factor (float): The shape factor of the internal elastomeric layers.
        type (str): The shape type of the bearing pad, default is 'rectangular', alternative is 'circular'.
        holes (bool): Indicates if the bearing pad has holes, default is False.
    """
    def __init__(self, width, length, durometer, internal_t, external_t, steel_t,
                 plys, span, expansion_length, loads, max_dl_delta, max_ll_delta, max_ll_loc, deck_slope, plate_bev,
                 edge_cover=.25, type='rectangular', holes=False, steel_yield_strength = 60, shear_modulus=0.095,
                 exp_coeff=.000006, temp_min=15, temp_max=95):
        self.width = width
        self.length = length
        self.durometer = durometer
        self.internal_t = internal_t
        self.external_t = external_t
        self.steel_t = steel_t
        self.plys = plys
        self.shear_modulus = shear_modulus
        self.exp_coeff = exp_coeff
        self.height = 2 * self.external_t + (self.plys - 1) * self.internal_t + (self.plys) * self.steel_t
        self.total_laminate_thickness = self.plys * self.steel_t
        self.total_elastomer_thickness = round(2 * self.external_t + (self.plys - 1) * self.internal_t, 2)
        self.span = span
        self.expansion_length = expansion_length
        self.f_y = steel_yield_strength  # (of the laminate layers)
        self.loads = loads
        self.sigma_l = None
        self.sigma_s = None
        self.delta_t = None
        self.delta_s = None
        self.dl_deflection = max_dl_delta
        self.ll_deflection = max_ll_delta
        self.ll_location = max_ll_loc
        self.deck_slope = deck_slope
        self.plate_bev = plate_bev
        self.temp_range = (temp_min, temp_max)
        self.get_deflections()
        self.edge_cover = edge_cover
        self.checks = {}
        self.internal_shape_factor = self.get_shape_factors(self.internal_t)
        self.service_ll = self.loads["total_load"] / (self.length * self.width)

        self.run_checks()

    def get_shape_factors(self, thickness):
        return (self.width * self.length) / (2 * thickness * (self.length + self.width))

    def run_checks(self):
        self.check_edge_cover()
        self.check_layer_thickness()
        # Excel Check '1' - Not Carried forward, see "Bearings" Notebook
        # Excel Check '2' (AASHTO 14.7.6.3.2-7)
        if self.service_ll <= 1.25 * self.shear_modulus * self.internal_shape_factor:
            self.checks['#2 - Service LL Check'] = 1
        else:
            self.checks['#2 - Service LL Check'] = 0
            print("Service LL Check Failed - Service LL > 1.25 * G * S_i")

        # Excel Check '3' (AASHTO 14.7.6.3.2-8)
        if self.service_ll <= 1.25:
            self.checks['#3 - Service LL < 1.25 ksi'] = 1
        else:
            self.checks['#3 - Service LL < 1.25 ksi'] = 0
            print("Service LL Check Failed - Service LL > 1.25 ksi")

        # Excel Check '4' (AASHTO 14.7.6.3.3-1)
        self.check_shape_factors()

        # //TODO - The way bearing stress is converted to strain isn't settled, figure out how to handle it for these 3
        # Excel Check '5' (AASHTO 14.7.6.3.3 & 14.7.5.3.6)
        self.checks['#5 - Needs Fixed'] = 1

        # Excel Check '6' (AASHTO 14.7.6.3.3 & 14.7.5.3.6)
        self.checks['#6 - Needs Fixed'] = 1

        # Excel Check '7' (AASHTO 14.7.6.3.3)
        self.checks['#7 - Needs Fixed'] = 1

        # Excel Check '8' (AASHTO 14.7.6.3.4)
        self.delta_t = self.exp_coeff * self.expansion_length * (self.temp_range[1] - self.temp_range[0]) * 12
        self.delta_s = self.delta_t
        if 2 * self.delta_s <= self.total_elastomer_thickness:
            self.checks['#8 - Thermal Expansion'] = 1
        else:
            self.checks['#8 - Thermal Expansion'] = 0
            print("Thermal expansion check failed, 2 * delta_s > h_ri")

        # Excel Check '9' (BDM 306.4)
        if self.total_elastomer_thickness < 5:
            self.checks['#9 - Maximum Elastomer height > 5\"'] = 1
        else:
            self.checks['#9 - Maximum Elastomer height > 5\"'] = 0
            print("Maximum Elastomer height check failed, total elastomer height > 5\"")

        # Excel Check '10' (BDM 306.4)
        if self.total_laminate_thickness < 1:
            self.checks['#10 - Maximum laminate height < 1\"'] = 1
        else:
            self.checks['#10 - Maximum laminate height < 1\"'] = 0
            print("Maximum laminate height check failed, total laminate height > 1\"")

        # Excel Check '11' (AASHTO 14.7.6.3.6)
        if self.width / 3 > self.total_laminate_thickness:
            self.checks['#11 - Laminate Width / 3 > Total Laminate Thickness'] = 1
        else:
            self.checks['#11 - Laminate Width / 3 > Total Laminate Thickness'] = 0
            print("Geometry Check Failed, Laminate Width / 3 > Total Laminate Thickness")

        # Excel Check '12' (AASHTO 14.7.6.3.6)
        if self.length / 3 > self.total_laminate_thickness:
            self.checks['#12 - Bearing Length / 3 > Total Laminate Thickness'] = 1
        else:
            self.checks['#12 - Bearing Length / 3 > Total Laminate Thickness'] = 0
            print("Geometry Check Failed, Bearing Length / 3 > Total Laminate Thickness")

        # Excel Check '13'
        if self.length * self.width < 1000:
            self.checks['#13 - Bearing Area < 1000'] = 1
        else:
            self.checks['#13 - Bearing Area < 1000'] = 0
            print("Geometry Check Failed, Bearing Length / 3 > Total Laminate Thickness")

        # Excel Check '14'
        if self.total_elastomer_thickness < 8:
            self.checks['#14 - Total elastomer thickness < 8\"'] = 1
        else:
            self.checks['#14 - Total elastomer thickness < 8\"'] = 0
            print("Geometry Check Failed, Bearing Length / 3 > Total Laminate Thickness")

        # Excel Check '15'
        H = self.shear_modulus * self.length * self.width * self.delta_t / self.total_elastomer_thickness
        if H < self.loads['total_dead_load']:
            self.checks['#15 - Total Dead Load'] = 1
        else:
            self.checks['#15 - Total Dead Load'] = 0
            print('Anchorage Check Failed, H < Total Dead Load, Anchorage is required')

        # Excel Check '16'
        if self.steel_t >= 3 * self.internal_t * self.sigma_s / self.f_y:
            self.checks['#16 - Steel Reinforcement - Service Limit State'] = 1
        else:
            self.checks['#16 - Steel Reinforcement - Service Limit State'] = 0
            print('Steel laminate service limit state check failed')

        # Excel Check 17
        if self.steel_t >= 2 * self.internal_t * self.sigma_l / 24:  # //TODO - Verify value doesn't change
            self.checks['#17 - Steel Reinforcement - Service Limit State'] = 1
        else:
            self.checks['#17 - Steel Reinforcement - Service Limit State'] = 0
            print('Steel laminate fatigue limit state check failed')

        # Excel Check 18
        gamma_a_st = 1.4 * self.sigma_s / (self.shear_modulus * 8)
        gamma_a_cy = 1.4 * self.sigma_l / (self.shear_modulus * 8)
        gamma_r_st = 0.5 * (self.length / self.internal_t) ** 2 * abs(
            (self.dl_deflection / (self.span * 12) + (self.deck_slope) + 0.005) / self.plys)
        gamma_r_cy = 0.5 * (self.length / self.internal_t) ** 2 * (abs(self.ll_deflection / (
                    self.ll_location * 12)) + 0.005) / self.plys  # //TODO - Check the formula for this one
        gamma_s_st = self.delta_s / self.total_elastomer_thickness
        gamma_s_cy = 0  # //TODO - Verify

        total_strains = (
                (gamma_a_st + gamma_r_st + gamma_s_st) + 1.75 * (
                    gamma_a_cy + gamma_r_cy + gamma_s_cy
                )
            )

        if total_strains < 5.0:
            self.checks['#18 - Total Strain'] = 1
        else:
            self.checks['#18 - Total Strain'] = 0
            print('Combined Strain Check Failed')

        # Excel Check 19
        gamma_r_st = 0.5 * (self.length / self.internal_t) ** 2 * abs(
            (self.dl_deflection / (self.span * 12) + (self.deck_slope - self.plate_bev) + 0.005) / self.plys)

        total_strains = (
                (gamma_a_st + gamma_r_st + gamma_s_st) + 1.75 * (
                gamma_a_cy + gamma_r_cy + gamma_s_cy
        )
        )
        if total_strains < 5.0:
            self.checks['#19 - Total Strain Check 2'] = 1
        else:
            self.checks['#19 - Total Strain Check 2'] = 0
            print('Combined Strain Check 2 Failed')

    def check_edge_cover(self):
        if self.edge_cover < .25:
            self.checks['Steel Laminate Edge Cover Check'] = 0
            print("Steel Laminate Edge Cover > 1/4\" - Failed")
        else:
            self.checks['Steel Laminate Edge Cover Check'] = 1

    def check_layer_thickness(self):
        if self.external_t > 5/16:
            self.checks['External Thickness Check > 5/16\"'] = 0
            print("External Thickness Check Failed - > 5/16\"")
        elif self.external_t > .7 * self.internal_t:
            self.checks['External Thickness > 70% Internal'] = 0
            print("External Thickness Check Failed - > 70% of Internal Thickness")
        else:
            self.checks['External Thickness Check > 5/16\"'] = 1
            self.checks['External Thickness > 70% Internal'] = 1

    def check_shape_factors(self):
        adjusted_plys = self.plys - 1  # Number of elastomeric layers is 1 less than steel plates

        # 14.7.6.1 - Count external layers as 1/2 if greater than half the thickness of internal
        if self.internal_t / 2 >= self.external_t:
            adjusted_plys = self.plys

        # Excel Check '4' (AASHTO 14.7.6.3.3-1)
        if self.internal_shape_factor ** 2 / adjusted_plys < 12:
            self.checks['#4 - Internal Shape Factor Check'] = 1
        else:
            self.checks['#4 - Internal Shape Factor Check'] = 0
            print("ShapeFactors Check Failed - Internal layer shape factor > 12 - Use Method A")

    def get_deflections(self):
        self.sigma_l = self.loads['live'] / (self.width * self.length)
        self.sigma_s = self.loads['total_dead_load'] / (self.width * self.length)

