import pandas as pd
import pint

units = pint.UnitRegistry()

steel_tables = pd.read_csv(
    'https://raw.githubusercontent.com/drparks71w/'
    'CivilPy/master/src/civilpy/structural/res/steel_shapes.csv')


def hello_world(user_input="World"):
    return f"Hello {user_input}!"


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
                  "check spelling and try again")


class WBeam(SteelSection):
    """
    Class to provide more specific attributes and functions related to designing
    with steel W beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = WBeam("W36X150")
    >>> t.weight
    150.0 pound/foot
    """

    def __init__(self, label):
        super(WBeam, self).__init__(label)
        self.depth = float(self.aisc_value['d'].values[0]) * units('in')
        self.detailing_depth = (
                float(self.aisc_value['ddet'].values[0]) * units('in')
        )
        self.flange_width = float(self.aisc_value['bf'].values[0]) * units('in')
        self.detailing_flange_width = (
                float(self.aisc_value['bfdet'].values[0]) * units('in')
        )
        self.web_thickness = (
                float(self.aisc_value['tw'].values[0]) * units('in')
        )
        self.detailing_web_thickness = (
                float(self.aisc_value['twdet'].values[0]) * units('in')
        )
        self.half_web_detail = (
                float(self.aisc_value['twdet/2'].values[0]) * units('in')
        )
        self.flange_thickness = (
                float(self.aisc_value['tf'].values[0]) * units('in')
        )
        self.detailing_flange_thickness = (
                float(self.aisc_value['tfdet'].values[0]) * units('in')
        )
        self.k_design = float(self.aisc_value['kdes'].values[0]) * units('in')
        self.k_detailing = (
                float(self.aisc_value['kdet'].values[0]) * units('in')
        )
        self.k1 = float(self.aisc_value['k1'].values[0]) * units('in')
        self.slenderness_ratio_flange = (
            float(self.aisc_value['bf/2tf'].values[0])
        )
        self.slenderness_ratio_web = float(self.aisc_value['h/tw'].values[0])
        self.J = float(self.aisc_value['J'].values[0]) * units('in^4')
        self.Cw = float(self.aisc_value['Cw'].values[0]) * units('in^6')
        self.Wno = float(self.aisc_value['Wno'].values[0]) * units('in^2')
        self.Sw1 = float(self.aisc_value['Sw1'].values[0]) * units('in^4')
        self.Qf = float(self.aisc_value['Qf'].values[0]) * units('in^3')
        self.Qw = float(self.aisc_value['Qw'].values[0]) * units('in^3')
        self.radius_of_gyration = self.rts = (
                float(self.aisc_value['rts'].values[0]) * units('in')
        )
        self.flange_centroid_distance = (
                float(self.aisc_value['ho'].values[0]) * units('in')
        )
        self.exposed_perimeter = (
                float(self.aisc_value['PA'].values[0]) * units('in')
        )
        self.shape_perimeter = (
                float(self.aisc_value['PB'].values[0]) * units('in')
        )
        self.box_perimeter = (
                float(self.aisc_value['PC'].values[0]) * units('in')
        )
        self.exposed_box_perimeter = (
                float(self.aisc_value['PD'].values[0]) * units('in')
        )
        self.web_face_depth = self.T = (
                float(self.aisc_value['T'].values[0]) * units('in')
        )
        self.fastener_workable_gage = self.WGi = (
                float(self.aisc_value['WGi'].values[0]) * units('in')
        )


class MBeam(WBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel M beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = MBeam("M10X9")
    >>> t.weight
    9.0 pound/foot
    """

    def __init__(self, label):
        super(MBeam, self).__init__(label)


class SBeam(WBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel M beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = SBeam("S24X121")
    >>> t.weight
    121.0 pound/foot
    """

    def __init__(self, label):
        super(SBeam, self).__init__(label)


class HPBeam(WBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel M beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = HPBeam("HP18X204")
    >>> t.weight
    204.0 pound/foot
    """

    def __init__(self, label):
        super(HPBeam, self).__init__(label)


class CBeam(WBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel C beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = CBeam("C15X50")
    >>> t.weight
    50.0 pound/foot
    """

    def __init__(self, label):
        super(CBeam, self).__init__(label)
        self.x = float(self.aisc_value['x'].values[0]) * units('in')
        self.eo = float(self.aisc_value['eo'].values[0]) * units('in')
        self.xp = float(self.aisc_value['xp'].values[0]) * units('in')
        self.slenderness_ratio = float(self.aisc_value['b/t'].values[0])
        self.warping_moment_2 = (
                float(self.aisc_value['Sw2'].values[0]) * units('in^4')
        )
        self.warping_moment_3 = (
                float(self.aisc_value['Sw3'].values[0]) * units('in^4')
        )
        self.ro = float(self.aisc_value['ro'].values[0]) * units('in')
        self.H = float(self.aisc_value['H'].values[0])


class MCBeam(CBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel MC beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = MCBeam("MC18X58")
    >>> t.weight
    58.0 pound/foot
    """

    def __init__(self, label):
        super(MCBeam, self).__init__(label)


class LBeam(CBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel L beams. Splitting values into multiple classes allows dropping
    of empty vain the database.

    >>> t = LBeam("L12x12x1-3/8")
    >>> t.weight
    105.0 pound/foot
    """

    def __init__(self, label):
        super(LBeam, self).__init__(label)
        self.b = float(self.aisc_value['b'].values[0]) * units('in')
        self.t = float(self.aisc_value['t'].values[0]) * units('in')
        self.y = float(self.aisc_value['y'].values[0]) * units('in')
        self.yp = float(self.aisc_value['yp'].values[0])
        self.Iz = float(self.aisc_value['Iz'].values[0]) * units('in^4')
        self.rz = float(self.aisc_value['rz'].values[0]) * units('in')
        self.Sz = float(self.aisc_value['Sz'].values[0]) * units('in^3')
        self.tan_a = float(self.aisc_value['tan(α)'].values[0])
        self.Iw = float(self.aisc_value['Iw'].values[0]) * units('in^4')
        self.zA = float(self.aisc_value['zA'].values[0]) * units('in')
        self.zB = float(self.aisc_value['zB'].values[0]) * units('in')
        self.zC = float(self.aisc_value['zC'].values[0]) * units('in')
        self.wA = float(self.aisc_value['wA'].values[0]) * units('in')
        self.wB = float(self.aisc_value['wB'].values[0]) * units('in')
        self.wC = float(self.aisc_value['wC'].values[0]) * units('in')
        self.SwA = float(self.aisc_value['SwA'].values[0]) * units('in^3')
        self.SwC = float(self.aisc_value['SwC'].values[0]) * units('in^3')
        self.SzA = float(self.aisc_value['SzA'].values[0]) * units('in^3')
        self.SzB = float(self.aisc_value['SzB'].values[0]) * units('in^3')
        self.SzC = float(self.aisc_value['SzC'].values[0]) * units('in^3')
        self.PA2 = float(self.aisc_value['PA2'].values[0]) * units('in')


class WTBeam(WBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel WT beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = WTBeam("WT22x145")
    >>> t.weight
    145.0 pound/foot
    """

    def __init__(self, label):
        super(WTBeam, self).__init__(label)
        self.d_t = float(self.aisc_value['D/t'].values[0])
        self.ro = float(self.aisc_value['ro'].values[0]) * units('in')
        self.y = float(self.aisc_value['y'].values[0]) * units('in')
        self.yp = float(self.aisc_value['yp'].values[0])
        self.H = float(self.aisc_value['H'].values[0])


class MTBeam(WTBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel WT beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = MTBeam("MT5x4")
    >>> t.weight
    4.0 pound/foot
    """

    def __init__(self, label):
        super(MTBeam, self).__init__(label)


class STBeam(WTBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel ST beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = STBeam("ST10x48")
    >>> t.weight
    48.0 pound/foot
    """

    def __init__(self, label):
        super(STBeam, self).__init__(label)


class TwoLBeam(WTBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel 2L beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = 2LBeam("2L10X10X1-1/4")
    >>> t.weight
    48.0 pound/foot
    """

    def __init__(self, label):
        super(STBeam, self).__init__(label)
        self.b = float(self.aisc_value['b'].values[0]) * units('in')
        self.t = float(self.aisc_value['t'].values[0]) * units('in')
        self.slenderness_ratio = float(self.aisc_value['b/t'].values[0])


class HSSBeam(WBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel HSS beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = HSSBeam("HSS20X20X.500")
    >>> t.weight
    130.52 pound/foot
    """

    def __init__(self, label):
        super(HSSBeam, self).__init__(label)
        self.tnom = float(self.aisc_value['tnom'].values[0]) * units('in')
        self.tdes = float(self.aisc_value['tdes'].values[0]) * units('in')
        self.C = float(self.aisc_value['C'].values[0]) * units('in^3')
        self.OD = float(self.aisc_value['OD'].values[0]) * units('in')
        self.ID = float(self.aisc_value['ID'].values[0]) * units('in')


class Pipe(HSSBeam):
    """
    Class to provide more specific attributes and functions related to designing
    with steel HSS beams. Splitting values into multiple classes allows dropping
    of empty values in the database.

    >>> t = Pipe("Pipe10SCH140")
    >>> t.weight
    104.0 pound/foot
    """

    def __init__(self, label):
        super(Pipe, self).__init__(label)
        self.OD = float(self.aisc_value['OD'].values[0]) * units('in')
        self.ID = float(self.aisc_value['ID'].values[0]) * units('in')
        self.D_t = float(self.aisc_value['D/t'].values[0])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
