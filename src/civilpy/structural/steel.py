import numpy as np
import pandas as pd
from civilpy.general import units
from civilpy.structural.res.definitions import A325_bolt_weights

steel_tables = pd.read_csv(
    'https://daneparks.com/Dane/civilpy/-/raw/master/src/civilpy/structural/res/steel_shapes.csv?ref_type=heads'
)


def hello_world(user_input="World"):
    return f"Hello {user_input}!"


def conv_frac_str(fraction_string: str) -> float:
    try:
        return float(fraction_string)
    except ValueError:
        num, denominator = fraction_string.split('/')
        try:
            leading, num = num.split()
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denominator)
        return whole - frac if whole < 0 else whole + frac


class SteelSection:
    """
    Main Steel Section Class, the goal is to make the attributes of various
    steel sections easily accessible in various python scripts.

    # //TODO - Add Rebar values
    """

    def __init__(self, label):
        self.id = self.clean_user_input(label)
        self.aisc_value = self.get_shape()

        self.special_note = self.aisc_value['T_F'].values[0]
        self.weight = self.W = self.aisc_value['W'].values[0] * units('lbf/ft')
        self.area = self.A = self.aisc_value['A'].values[0] * units('in^2')
        self.I_x = self.aisc_value['Ix'].values[0] * units('in^4')
        self.Z_x = self.aisc_value['Zx'].values[0] * units('in^3')
        self.S_x = self.aisc_value['Sx'].values[0] * units('in^3')
        self.r_x = self.aisc_value['rx'].values[0] * units('in')
        self.I_y = self.aisc_value['Iy'].values[0] * units('in^4')
        self.Z_y = self.aisc_value['Zy'].values[0] * units('in^3')
        self.S_y = self.aisc_value['Sy'].values[0] * units('in^3')
        self.r_y = self.aisc_value['ry'].values[0] * units('in')

    def clean_user_input(self, user_input):
        """
        Eliminates value not found errors by removing lower case letters and
        spaces

        >>> t = SteelSection("W 44X335")
        >>> print(t.clean_user_input('W 44X335'))
        W44X335
        >>> print(t.clean_user_input('w40x294'))
        W40X294
        >>> t.id
        'W40X294'

        :return: cleaned input
        """

        if user_input[0:4].lower() == 'pipe':
            no_spaces = user_input.replace(' ', '')
            cleaned_input = no_spaces
            self.id = cleaned_input
        else:
            no_spaces = user_input.replace(' ', '')
            cleaned_input = no_spaces.upper()
            self.id = cleaned_input

        return cleaned_input

    def get_shape(self):
        """
        Searches AISC Steel database table for member label passed to it,
        returns values from table if it finds a match, or prints an error if it
        doesn't

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
            shape_values = steel_tables[
                steel_tables['EDI_Std_Nomenclature'] == self.id]
            return shape_values
        except KeyError as e:
            print("Value not found in shape table,"
                  "check spelling and try again"
                  f"\n\n{e}")


class W(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel W s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = W("W36X150")
    >>> t.weight
    150.0 pound/foot
    """

    def __init__(self, label):
        super(W, self).__init__(label)
        self.depth = (
                conv_frac_str(self.aisc_value['d'].values[0]) * units('in')
            )
        self.detailing_depth = (
                conv_frac_str(self.aisc_value['ddet'].values[0]) * units('in')
            )
        self.flange_width = (
                conv_frac_str(self.aisc_value['bf'].values[0]) * units('in')
            )
        self.detailing_flange_width = conv_frac_str(self.aisc_value['bfdet'].values[0]) * units('in')
        self.web_thickness = (
                    conv_frac_str(self.aisc_value['tw'].values[0]) * units('in')
            )
        self.detailing_web_thickness = conv_frac_str(self.aisc_value['twdet'].values[0]) * units('in')
        self.half_web_detail = (
                conv_frac_str(self.aisc_value['twdet/2'].values[0]) * units('in')
        )
        self.flange_thickness = (
                conv_frac_str(self.aisc_value['tf'].values[0]) * units('in')
        )
        self.detailing_flange_thickness = (
                conv_frac_str(self.aisc_value['tfdet'].values[0]) * units('in')
        )
        self.k_design = conv_frac_str(self.aisc_value['kdes'].values[0]) * units('in')
        self.k_detailing = (
                conv_frac_str(self.aisc_value['kdet'].values[0]) * units('in')
        )
        self.slenderness_ratio_web = conv_frac_str(self.aisc_value['h/tw'].values[0])
        self.J = conv_frac_str(self.aisc_value['J'].values[0]) * units('in^4')
        self.Cw = conv_frac_str(self.aisc_value['Cw'].values[0]) * units('in^6')
        self.Wno = conv_frac_str(self.aisc_value['Wno'].values[0]) * units('in^2')
        self.Sw1 = (
                conv_frac_str(self.aisc_value['Sw1'].values[0]) * units('in^4')
            )
        self.Qf = conv_frac_str(self.aisc_value['Qf'].values[0]) * units('in^3')
        self.Qw = conv_frac_str(self.aisc_value['Qw'].values[0]) * units('in^3')
        self.radius_of_gyration = self.rts = (
                conv_frac_str(self.aisc_value['rts'].values[0]) * units('in')
        )
        self.flange_centroid_distance = (
                conv_frac_str(self.aisc_value['ho'].values[0]) * units('in')
        )
        self.exposed_perimeter = (
                conv_frac_str(self.aisc_value['PA'].values[0]) * units('in')
        )
        self.shape_perimeter = (
                conv_frac_str(self.aisc_value['PB'].values[0]) * units('in')
        )
        self.box_perimeter = (
                conv_frac_str(self.aisc_value['PC'].values[0]) * units('in')
        )
        self.exposed_box_perimeter = (
                conv_frac_str(self.aisc_value['PD'].values[0]) * units('in')
        )
        self.web_face_depth = self.T = (
                conv_frac_str(self.aisc_value['T'].values[0]) * units('in')
        )

        # These values are used in most shapes, but not all, hence the ifs
        self.slenderness_ratio_flange = (
                conv_frac_str(self.aisc_value['bf/2tf'].values[0]) * units('in')
        )
        self.k1 = (
                conv_frac_str(self.aisc_value['k1'].values[0]) * units('in')
        )

        self.fastener_workable_gage = (
                conv_frac_str(self.aisc_value['WGi'].values[0]) * units('in')
        )


class M(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel M s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = M("M10X9")
    >>> t.weight
    9.0 pound/foot
    """

    def __init__(self, label):
        super(M, self).__init__(label)


class S(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel M s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = S("S24X121")
    >>> t.weight
    121.0 pound/foot
    """

    def __init__(self, label):
        super(S, self).__init__(label)


class HP(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel M s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = HP("HP18X204")
    >>> t.weight
    204.0 pound/foot
    """

    def __init__(self, label):
        super(HP, self).__init__(label)


class C(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel C s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = C("C15X50")
    >>> t.weight
    50.0 pound/foot
    """

    def __init__(self, label):
        super(C, self).__init__(label)
        self.x = conv_frac_str(self.aisc_value['x'].values[0]) * units('in')
        self.eo = conv_frac_str(self.aisc_value['twdet'].values[0]) * units('in')
        self.xp = conv_frac_str(self.aisc_value['xp'].values[0]) * units('in')
        self.slenderness_ratio = conv_frac_str(self.aisc_value['b/t'].values[0])
        self.warping_moment_2 = conv_frac_str(self.aisc_value['Sw2'].values[0]) * units('in^4')
        self.warping_moment_3 = conv_frac_str(self.aisc_value['Sw3'].values[0]) * units('in^4')
        self.ro = conv_frac_str(self.aisc_value['ro'].values[0]) * units('in')
        self.H = conv_frac_str(self.aisc_value['H'].values[0])


class MC(C):
    """
    Class to provide more specific attributes and functions related to designing
    with steel MC s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = MC("MC18X58")
    >>> t.weight
    58.0 pound/foot
    """

    def __init__(self, label):
        super(MC, self).__init__(label)


class L(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel L s. Splitting values into multiple classes allows dropping
    of empty vain the database.

    >>> t = L("L12x12x1-3/8")
    >>> t.weight
    105.0 pound/foot
    """

    def __init__(self, label):
        super(L, self).__init__(label)
        self.b = conv_frac_str(self.aisc_value['b'].values[0]) * units('in')
        self.t = conv_frac_str(self.aisc_value['t'].values[0]) * units('in')
        self.y = conv_frac_str(self.aisc_value['y'].values[0]) * units('in')
        self.yp = conv_frac_str(self.aisc_value['yp'].values[0])
        self.Iz = conv_frac_str(self.aisc_value['Iz'].values[0]) * units('in^4')
        self.rz = conv_frac_str(self.aisc_value['rz'].values[0]) * units('in')
        self.Sz = conv_frac_str(self.aisc_value['Sz'].values[0]) * units('in^3')
        self.tan_a = conv_frac_str(self.aisc_value['tan(α)'].values[0])
        self.Iw = conv_frac_str(self.aisc_value['Iw'].values[0]) * units('in^4')
        self.zA = conv_frac_str(self.aisc_value['zA'].values[0]) * units('in')
        self.zB = conv_frac_str(self.aisc_value['zB'].values[0]) * units('in')
        self.zC = conv_frac_str(self.aisc_value['zC'].values[0]) * units('in')
        self.wA = conv_frac_str(self.aisc_value['wA'].values[0]) * units('in')
        self.wB = conv_frac_str(self.aisc_value['wB'].values[0]) * units('in')
        self.wC = conv_frac_str(self.aisc_value['wC'].values[0]) * units('in')
        self.SwA = conv_frac_str(self.aisc_value['SwA'].values[0]) * units('in^3')
        self.SwC = conv_frac_str(self.aisc_value['SwC'].values[0]) * units('in^3')
        self.SzA = conv_frac_str(self.aisc_value['SzA'].values[0]) * units('in^3')
        self.SzB = conv_frac_str(self.aisc_value['SzB'].values[0]) * units('in^3')
        self.SzC = conv_frac_str(self.aisc_value['SzC'].values[0]) * units('in^3')
        self.PA2 = conv_frac_str(self.aisc_value['PA2'].values[0]) * units('in')


class WT(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel WT s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = WT("WT22x145")
    >>> t.weight
    145.0 pound/foot
    """

    def __init__(self, label):
        super(WT, self).__init__(label)
        self.d_t = conv_frac_str(self.aisc_value['D/t'].values[0])
        self.ro = conv_frac_str(self.aisc_value['ro'].values[0]) * units('in')
        self.y = conv_frac_str(self.aisc_value['y'].values[0]) * units('in')
        self.yp = conv_frac_str(self.aisc_value['yp'].values[0])
        self.H = conv_frac_str(self.aisc_value['H'].values[0])


class MT(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel WT s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = MT("MT5x4")
    >>> t.weight
    4.0 pound/foot
    """

    def __init__(self, label):
        super(MT, self).__init__(label)


class ST(WT):
    """
    Class to provide more specific attributes and functions related to designing
    with steel ST s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = ST("ST10x48")
    >>> t.weight
    48.0 pound/foot
    """

    def __init__(self, label):
        super(ST, self).__init__(label)


class TwoL(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel 2L s. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = TwoL("2L10X10X1-1/4")
    >>> t.weight
    48.0 pound/foot
    """

    def __init__(self, label):
        super(TwoL, self).__init__(label)
        self.b = conv_frac_str(self.aisc_value['b'].values[0]) * units('in')
        self.t = conv_frac_str(self.aisc_value['t'].values[0]) * units('in')
        self.slenderness_ratio = conv_frac_str(self.aisc_value['b/t'].values[0])


class HSS(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel HSS sections. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = HSS("HSS20X20X.500")
    >>> t.weight
    130.52 pound/foot
    """

    def __init__(self, label):
        super(HSS, self).__init__(label)
        self.tnom = conv_frac_str(self.aisc_value['tnom'].values[0]) * units('in')
        self.tdes = conv_frac_str(self.aisc_value['tdes'].values[0]) * units('in')
        self.C = conv_frac_str(self.aisc_value['C'].values[0]) * units('in^3')
        if self.aisc_value['OD'].values[0] == '–':
            self.OD = None
        else:
            self.OD = conv_frac_str(self.aisc_value['OD'].values[0]) * units('in')
        if self.aisc_value['ID'].values[0] == '–':
            self.ID = None
        else:
            self.ID = conv_frac_str(self.aisc_value['ID'].values[0]) * units('in')


class Pipe(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel Pipe Sections. Splitting values into multiple classes allows
    dropping of empty values in the database.

    >>> t = Pipe("Pipe10SCH140")
    >>> t.weight
    104.0 pound/foot
    """

    def __init__(self, label):
        super(Pipe, self).__init__(label)
        self.OD = conv_frac_str(self.aisc_value['OD'].values[0]) * units('in')
        self.ID = conv_frac_str(self.aisc_value['ID'].values[0]) * units('in')
        self.D_t = conv_frac_str(self.aisc_value['D/t'].values[0])


def get_bolt_weights(length: float, diameter: float, no_of_washers: int) -> float:
    """
    Function to get the bolt weights from the A325_bolt_weights dictionary and calculate the weight per bolt if it's
    not contained in the table.

    Original table from:
    https://www.portlandbolt.com/print/?table=7587

    The A325_bolt_weights dictionary reports the weight indexed by bolt length and diameter, and reports the value in
    lbs/100 bolts. This function simplifies that by reducing the value to that of a single bolt.

    If bolt weights are not contained in the dictionary, the function will utilize the following formula to calculate
    the weight per bolt, if no_of_washers is greater than 0, it will include the weight of the washers in the
    calculation with the following values:

    Per inch Adder (dia):
        0.5: 5.5
        0.625: 8.6
        0.75: 12.4
        0.875: 16.9
        1.0: 22.1
        1.125: 28
        1.25: 34.4
        1.375: 42.5
        1.5: 49.7

    F436 Round Washers
        0.5: 2.1
        0.625: 3.6
        0.75: 4.8
        0.875: 7
        1.0: 9.4
        1.125: 11.3
        1.25: 13.8
        1.375: 16.8
        1.5: 20

    Weight in table includes the weight of nuts.

    Parameters
    -------
    length : float
    diameter : float
    no_of_washers : int

    Returns
    -------
    Weight : float - the weight of the individual bolt
    """

    # Test if the inputs are in the table or if the formula must be used to calculate weight
    if length in A325_bolt_weights.keys() and diameter in A325_bolt_weights[9].keys():
        total_weight = A325_bolt_weights[length][diameter]

    # Make sure user input is one of the available diameters
    elif diameter not in A325_bolt_weights[9].keys() or length not in A325_bolt_weights.keys():
        print('\nNon-existant diameter or length used, please use a value from the following list:')
        print('\n\t0.5\n\t0.625\n\t0.75\n\t0.875\n\t1.0\n\t1.125\n\t1.25\n\t1.375\n\t1.5\n\n')

        return None

    # Calculates the weight of bolts longer than 9", uses 6" bolt to have all dias
    elif diameter in A325_bolt_weights[9].keys() and length > max(A325_bolt_weights.keys()):
        length_adder = {
            0.5: 5.5,
            0.625: 8.6,
            0.75: 12.4,
            0.875: 16.9,
            1.0: 22.1,
            1.125: 28,
            1.25: 34.4,
            1.375: 42.5,
            1.5: 49.7
        }

        added_length = length - 6
        total_weight = A325_bolt_weights[6][diameter] + added_length * length_adder[diameter]

    # Adds washer weight if no of washers > 0
    for washer in range(0, no_of_washers, 1):
        washer_weight = {
            0.5: 2.1,
            0.625: 3.6,
            0.75: 4.8,
            0.875: 7,
            1.0: 9.4,
            1.125: 11.3,
            1.25: 13.8,
            1.375: 16.8,
            1.5: 20,
        }

        total_weight = total_weight + washer_weight[diameter]

    return round((total_weight / 100), 3) * units.lbs


if __name__ == '__main__':
    import doctest
    doctest.testmod()
