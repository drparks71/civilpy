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
    def __init__(self, width, length, height, durometer, internal_t, external_t, steel_t,
                 plys, edge_cover=.25, type='rectangular', holes=False):
        self.width = width
        self.length = length
        self.height = height
        self.durometer = durometer
        self.internal_t = internal_t
        self.external_t = external_t
        self.steel_t = steel_t
        self.plys = plys
        self.edge_cover = edge_cover
        self.checks = {}
        self.internal_shape_factor = self.get_shape_factors(self.internal_t)

        self.check_layer_thickness()
        self.check_edge_cover()
        self.check_shape_factors()

    def get_shape_factors(self, thickness):
        return (self.width * self.length) / (2 * thickness * (self.length + self.width))

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
        if self.internal_shape_factor ** 2 / adjusted_plys > 22:
            self.checks['Internal Shape Factor Check'] = 0
            print("ShapeFactors Check Failed - Internal layer shape factor > 22 - Use Method A")
        else:
            self.checks['Internal Shape Factor Check'] = 1

    def check_edge_cover(self):
        if self.edge_cover < .25:
            self.checks['Steel Laminate Edge Cover Check'] = 0
            print("Steel Laminate Edge Cover > 1/4\" - Failed")
        else:
            self.checks['Steel Laminate Edge Cover Check'] = 1


class HL93Load:
    def __init__(self):
        self.axels = {
            'spacing': 6,
            1: {'load': 8, 'dist': 0},
            2: {'load': 32, 'dist': 14},
            3: {'load': 32, 'dist': [14, 30]}
        }


