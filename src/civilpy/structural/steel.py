import pandas as pd
import pint

units = pint.UnitRegistry()

steel_tables = pd.read_csv('https://raw.githubusercontent.com/drparks71w/CivilPy/master/civilpy/structural/res/steel_shapes.csv')


def hello_world(user_input="World"):
    return f"Hello {user_input}!"


class SteelSection:
    """
    Main Steel Section Class, the goal is to make the attributes of various steel
    sections easily accessible in various python scripts.

    # //TODO - Add Rebar values
    # //TODO - Integrate Units
    # //TODO - Metric toggle
    # //TODO - Add Definitions for members other than W-Shapes
    """

    def __init__(self, label):
        self.id = self.clean_user_input(label)
        self.aisc_value = self.get_shape()

        self.special_note = self.aisc_value['T_F'].values[0]
        self.weight = self.aisc_value['W'].values[0]    # lb/ft (kg/m)
        self.area = self.aisc_value['A'].values[0]      # in^2  (mm^2)
        self.I_x = self.aisc_value['Ix'].values[0]      # in^4  (mm^4 / 10^6)
        self.Z_x = self.aisc_value['Zx'].values[0]      # in^3  (mm^3 / 10^3)
        self.S_x = self.aisc_value['Sx'].values[0]      # in^3  (mm^3 / 10^3)
        self.r_x = self.aisc_value['rx'].values[0]      # in    (mm)
        self.I_y = self.aisc_value['Iy'].values[0]      # in^4  (mm^4/10^6)
        self.Z_y = self.aisc_value['Zy'].values[0]      # in^3  (mm^3/10^3)
        self.S_y = self.aisc_value['Sy'].values[0]      # in^3  (mm^3/10^3)
        self.r_y = self.aisc_value['ry'].values[0]      # in    (mm)

    def clean_user_input(self, user_input):
        """
        Eliminates value not found errors by removing lower case letters and spaces

        >>> t = SteelSection("W 44X335")
        >>> print(t.clean_user_input('W 44X335'))
        W44X335
        >>> print(t.clean_user_input('w40x294'))
        W40X294
        >>> t.id
        'W40X294'

        :return: cleaned input
        """

        no_spaces = user_input.replace(' ', '')
        cleaned_input = no_spaces.upper()
        self.id = cleaned_input

        return cleaned_input

    def get_shape(self):
        """
        Searches AISC Steel database table for member label passed to it, returns values
        from table if it finds a match, or prints an error if it doesn't

        >>> t = SteelSection("W36X150")
        >>> t.aisc_value['Type'].values[0]
        'W'

        >>> t = SteelSection("2L8X4X5/8LLBB")
        >>> t.aisc_value['W'].values[0]
        48.4

        :param self:
        :return: dataframe of raw values from AISC Shape Table
        """
        try:
            shape_values = steel_tables[steel_tables['EDI_Std_Nomenclature'] == self.id]
            return shape_values
        except KeyError as e:
            print("Value not found in shape table, check spelling and try again")


class WBeam(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing with
    steel W beams. Splitting values into multiple classes allows dropping of empty values
    in the database.

    >>> t = WBeam("W36X150")
    >>> t.weight
    150.0
    """
    def __init__(self, label):
        super(WBeam, self).__init__(label)
        self.depth = float(self.aisc_value['d'].values[0]) * units.inch                    # in (mm)
        self.detailing_depth = float(self.aisc_value['ddet'].values[0]) * units.inch             # in (mm)
        self.flange_width = float(self.aisc_value['bf'].values[0]) * units.inch                   # in (mm)
        self.detailing_flange_width = float(self.aisc_value['bfdet'].values[0]) * units.inch      # in (mm)
        self.web_thickness = float(self.aisc_value['tw'].values[0])                  # in (mm)
        self.detailing_web_thickness = float(self.aisc_value['twdet'].values[0])     # in (mm)
        self.half_web_detail = float(self.aisc_value['twdet/2'].values[0])           # in (mm)
        self.flange_thickness = float(self.aisc_value['tf'].values[0])               # in (mm)
        self.detailing_flange_thickness = float(self.aisc_value['tfdet'].values[0])  # in (mm)
        self.k_design = float(self.aisc_value['kdes'].values[0])                     # in (mm)
        self.k_detailing = float(self.aisc_value['kdet'].values[0])                  # in (mm)
        self.k1 = float(self.aisc_value['k1'].values[0])                             # in (mm)
        self.slenderness_ratio_flange = float(self.aisc_value['bf/2tf'])
        self.slenderness_ratio_web = float(self.aisc_value['h/tw'])
        self.J = float(self.aisc_value['J'])                                         # in^4 (mm^4 / 10^3)
        self.Cw = float(self.aisc_value['Cw'])                                        # in^6 (mm^6 / 10^9)
        self.Wno = float(self.aisc_value['Wno'])                                     # in^2 (mm^2)
        self.Sw1 = float(self.aisc_value['Sw1'])                                     # in^4 (mm^4 / 10^6)
        self.Qf = float(self.aisc_value['Qf'])                                       # in^3 (mm^3 / 10^3)
        self.Qw = float(self.aisc_value['Qw'])                                    # in^3 (mm^3 / 10^3)
        self.radius_of_gyration = self.rts = float(self.aisc_value['rts'])         # in (mm)
        self.flange_centroid_distance = float(self.aisc_value['ho'])              # in (mm)
        self.exposed_perimeter = float(self.aisc_value['PA'])                     # in (mm)
        self.shape_perimeter = float(self.aisc_value['PB'])                       # in (mm)
        self.box_perimeter = float(self.aisc_value['PC'])                         # in (mm)
        self.exposed_box_perimeter = float(self.aisc_value['PD'])                 # in (mm)
        self.web_face_depth = self.T = float(self.aisc_value['T'])                # in (mm)
        self.fastener_workable_gage = self.WGi =  float(self.aisc_value['WGi'])   # in (mm)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
