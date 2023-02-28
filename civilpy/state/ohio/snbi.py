import sys
import pint
from civilpy.state.ohio.dot import get_cty_from_code, state_code_conversion, get_3_digit_st_cd_from_2
from civilpy.state.ohio.dot import ohio_counties, convert_latitudinal_values, convert_place_code
from civilpy.state.ohio.dot import convert_longitudinal_values, TimsBridge, get_historic_bridge_data

units = pint.UnitRegistry()


class SNBITransfer(TimsBridge):
    def __init__(self, sfn):
        """
        This init function runs every "check" of the historic value vs. the modern
        and saves the result to its own dictionary attribute 'transition_record'
        within the class object as well as printing out the results.

        Currently, inherits attributes from the ODOT TimsBridge object as the source
        of truth for modern values, and the NBI historic records downloads from
        2022 for the "historic" values at:

        "https://daneparks.com/Dane/civilpy/-/raw/snibi_tests_development/res/Ohio_NBI.txt

        Args:
            sfn (str): The structure file number used to identify the bridge for
                the lookup of values for modern and historic data

        Returns:
            SNBITransfer object, which includes a list of check results under the
            attribute SNBITransfer.transition_record
        """

        if type(sfn) != str:
            sfn = str(sfn)

        super().__init__(sfn)
        self.historic_data = get_historic_bridge_data(sfn)

        print("Starting SNBI Transfer Checks")
        self.transition_record = {
            'BID01': self.bid01(),
            'BID02': self.bid02(),
            'BID03': self.bid03(),
            'BL01': self.bl01(),
            'BL02': self.bl02(),
            'BL03': self.bl03(),
            'BL04': self.bl04(),
            'BL05': self.bl05(),
            'BL06': self.bl06(),
            'BL07': self.bl07(),
            'BL08': self.bl08(),
            'BL09': self.bl09(),
            'BL10': self.bl10(),
            'BL11': self.bl11(),
            'BL12': self.bl12(),
            'BCL01': self.bcl01(),
            'BCL02': self.bcl02(),
            'BCL03': self.bcl03(),
            'BCL04': self.bcl04(),
            'BCL05': self.bcl05(),
            'BCL06': self.bcl06(),
            'BSP01': self.bsp01(),
            'BSP02': self.bsp02(),
            'BSP03': self.bsp03(),
            'BSP04': self.bsp04(),
            'BSP05': self.bsp05(),
            'BSP06': self.bsp06(),
            'BSP07': self.bsp07(),
            'BSP08': self.bsp08(),
            'BSP09': self.bsp09(),
            'BSP10': self.bsp10(),
            'BSP11': self.bsp11(),
            'BSP12': self.bsp12(),
            'BSP13': self.bsp13(),
            'BSB01': self.bsb01(),
            'BSB02': self.bsb02(),
            'BSB03': self.bsb03(),
            'BSB04': self.bsb04(),
            'BSB05': self.bsb05(),
            'BSB06': self.bsb06(),
            'BSB07': self.bsb07(),
            'BRH01': self.brh01(),
            'BRH02': self.brh02(),
            'BG01': self.bg01(),
            'BG02': self.bg02(),
            'BG03': self.bg03(),
            'BG04': self.bg04(),
            'BG05': self.bg05(),
            'BG06': self.bg06(),
            'BG07': self.bg07(),
            'BG08': self.bg08(),
            'BG09': self.bg09(),
            'BG10': self.bg10(),
            'BG11': self.bg11(),
            'BG12': self.bg12(),
            'BG13': self.bg13(),
            'BG14': self.bg14(),
            'BG15': self.bg15(),
            'BG16': self.bg16(),
            'BF01': self.bf01(),
            'BF02': self.bf02(),
            'BF03': self.bf03(),
            'BRT01': self.brt01(),
            'BRT02': self.brt02(),
            'BRT03': self.brt03(),
            'BRT04': self.brt04(),
            'BRT05': self.brt05(),
            'BH01': self.bh01(),
            'BH02': self.bh02(),
            'BH03': self.bf03(),
            'BH04': self.bf03(),
            'BH05': self.bf03(),
            'BH06': self.bf03(),
            'BH07': self.bf03(),
            'BH08': self.bf03(),
            'BH09': self.bf03(),
            'BH10': self.bf03(),
            'BH11': self.bf03(),
            'BH12': self.bf03(),
            'BH13': self.bf03(),
            'BH14': self.bf03(),
            'BH15': self.bf03(),
            'BH16': self.bf03(),
            'BH17': self.bf03(),
            'BH18': self.bf03(),
            'BRR01': self.brr01(),
            'BRR02': self.brr02(),
            'BRR03': self.brr03(),
            'BN01': self.bn01(),
            'BN02': self.bn02(),
            'BN03': self.bn03(),
            'BN04': self.bn04(),
            'BN05': self.bn05(),
            'BN06': self.bn06(),
            'BLR01': self.blr01(),
            'BLR02': self.blr02(),
            'BLR03': self.blr03(),
            'BLR04': self.blr04(),
            'BLR05': self.blr05(),
            'BLR06': self.blr06(),
            'BLR07': self.blr07(),
            'BLR08': self.blr08(),
            'BPS01': self.bps01(),
            'BPS02': self.bps02(),
            'BEP01': self.bep01(),
            'BEP02': self.bep02(),
            'BEP03': self.bep03(),
            'BEP04': self.bep04(),
            'BIR01': self.bir01(),
            'BIR02': self.bir02(),
            'BIR03': self.bir03(),
            'BIR04': self.bir04(),
            'BIE01': self.bie01(),
            'BIE02': self.bie02(),
            'BIE03': self.bie03(),
            'BIE04': self.bie04(),
            'BIE05': self.bie05(),
            'BIE06': self.bie06(),
            'BIE07': self.bie07(),
            'BIE08': self.bie08(),
            'BIE09': self.bie09(),
            'BIE10': self.bie10(),
            'BIE11': self.bie11(),
            'BIE12': self.bie12(),
            'BC01': self.bc01(),
            'BC02': self.bc02(),
            'BC03': self.bc03(),
            'BC04': self.bc04(),
            'BC05': self.bc05(),
            'BC06': self.bc06(),
            'BC07': self.bc07(),
            'BC08': self.bc08(),
            'BC09': self.bc09(),
            'BC10': self.bc10(),
            'BC11': self.bc11(),
            'BC12': self.bc12(),
            'BC13': self.bc13(),
            'BC14': self.bc14(),
            'BC15': self.bc15(),
            'BAP01': self.bap01(),
            'BAP02': self.bap02(),
            'BAP03': self.bap03(),
            'BAP04': self.bap04(),
            'BAP05': self.bap05(),
            'BW01': self.bw01(),
            'BW02': self.bw02(),
            'BW03': self.bw03(),
        }

    def bid01(self, historic: str = '', modern: str = '', leading_zeros: int = 0):
        """
        B.ID.01 Function - Bridge Number Comparison

        Compares historically reported SFN to its modern value

        Parameters:
            historic (str): Historic value used in comparison, for this function,
            the value in the historical value dictionary stored at:
                historic_data["STRUCTURE_NUMBER_008"]

            modern (str): The value stored in the modern bridge object as the
            attribute BridgeObject.sfn

            leading_zeros (int): The number of leading zeros a state chooses to
            use in their naming conventions, Ohio doesn't use them, if you do,
            you should stop, but if you insist, look into zfill.

        Returns:
            If the value is what was expected returns None, if they are different
            returns both values with an error message as a string
        """

        # Assign Historic and Modern Values, the logic statements allow the
        # function to be tested outside of being run as part of a transition
        if historic == '':
            historic = self.historic_data["STRUCTURE_NUMBER_008"].iloc[0].strip()

            # Prints an error if the historic value is not a string as expected
            if type(historic) != str:
                print("Expected a string stored in the historic record for SFN")

            leading_zeros_var = leading_zeros
            print(f'Running transition with leading_zeros set to: {leading_zeros_var}')

            modern = self.sfn
        else:
            historic = historic
            modern = modern

        # Check Equivalency
        if historic == modern:
            return_var = None
        else:
            print(f"'B.ID_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto match")
            return_var = 'B.ID_01_CHECK_FAILED'

        return return_var

    def bid02(self):
        """
        B.ID.02 Function - Bridge Name

        Previously didn't exist - Created as placeholder, does nothing
        """
        # //TODO - Determine if there's any checks to run here against modern values
        pass

    def bid03(self, historic: str = '', modern: str = ''):
        """
        B.ID.03 Function - Previous Bridge Number

        Previously didn't exist - Created as placeholder, does nothing
        """
        # //TODO - Determine if there's any checks to run here against modern values
        pass

    def bl01(self, historic: str = '', modern: str = '',  state: str = 'Ohio'):
        """
        B.L.01 Function - State Code Comparison

        This is the first of the more complex functions, relies on two functions defined in
        dot.py, 'state_code_conversion' and 'get_3_digit_st_cd_from_2', converts the historic
        2 digit state code to a 3-digit code, which gets converted to the plain text
        state name.

        The default state value is set to Ohio, this determines the modern value the function
        will check against.

        Parameters:
            historic (str): Historic value used in comparison, for this function,
            the value in the historical value dictionary stored at:
                historic_data["STATE_CODE_001"]

            modern (str): The value stored in the modern bridge object as the
            attribute BridgeObject.sfn

            state (str): The default state to use while

        Returns:
            If the value is what was expected returns None, if they are different
            returns both values with an error message as a string
        """

        # Allows for overriding values for testing
        if historic == '':
            historic = state_code_conversion(get_3_digit_st_cd_from_2(self.historic_data["STATE_CODE_001"].iloc[0]))
            modern = state
        else:
            pass

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto match")
            return_var = 'BL_01_CHECK_FAILED'

        return return_var

    def bl02(self, historic: str = '', modern: str = ''):
        """
        B.L.02 Function - County Code Comparison


        """
        if historic == '':
            county_name = get_cty_from_code(
                self.historic_data["COUNTY_CODE_003"].iloc[0],
                self.historic_data["STATE_CODE_001"].iloc[0])
            county_short = county_name.split(' ')[0]
            historic = ohio_counties[county_short.upper()]

            modern = self.county_cd
        else:
            pass

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto match")
            return_var = 'BL_02_CHECK_FAILED'

        return return_var

    def bl03(self):
        """
        B.L.03 Function - Place Code Comparison
        """
        historic = str(self.historic_data["PLACE_CODE_004"].iloc[0])

        modern = self.fips_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto match\nAttempted Conversion: {convert_place_code(self.fips_cd)}")
            return_var = 'BL_03_CHECK_FAILED'

        return return_var

    def bl04(self):
        """
        B.L.04 Function - Highway Agency District
        """
        historic = str(self.historic_data["HIGHWAY_DISTRICT_002"].iloc[0])
        modern = self.district

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto match\n")
            return_var = 'BL_04_CHECK_FAILED'

        return return_var

    def bl05(self):
        """
        B.L.05 Function - Latitude
        """
        historic = float(convert_latitudinal_values(self.historic_data["LAT_016"].iloc[0]))
        modern = self.latitude_dd

        # Gets the error from the new and old latitude in feet (estimate based on equator) returns an error if over
        # 500'
        error_magnitude = abs(
            (modern - historic) / 2.7e-6
        )

        if error_magnitude < 50:
            return_var = None
        else:
            print(f"'BL_05_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be less than 50' apart\n")
            return_var = 'BL_05_CHECK_FAILED'

        return return_var

    def bl06(self):
        """
        B.L.06 Function - Longitude
        """
        historic = float(convert_longitudinal_values(self.historic_data["LONG_017"].iloc[0]))
        modern = self.longitude_dd

        # Gets the error from the new and old latitude in feet (estimate based on the equator) returns an error if over
        # 500'
        error_magnitude = abs(
            (modern - historic) / 5.9e-6
        )

        if error_magnitude < 50:
            return_var = None
        else:
            print(f"'BL_06_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be less than 50' apart\n")
            return_var = 'BL_06_CHECK_FAILED'

        return return_var

    def bl07(self):
        """
        B.L.07 Function - Border Bridge Number
        """
        historic = self.historic_data["OTHR_STATE_STRUC_NO_099"].iloc[0]
        modern = self.brdr_brg_sfn

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BL_07_CHECK_FAILED'

        return return_var

    def bl08(self):
        """
        B.L.08 Function - Border Bridge State or Country Code
        """
        historic = self.historic_data["OTHER_STATE_CODE_098A"].iloc[0]
        modern = self.brdr_brg_state

        if historic == modern:
            return_var = None
        else:
            try:
                print(f"'BL_08_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                      f"Modern: {modern}\n\nto be equal\nCode Conversion: {state_code_conversion(modern)}\n\n")
                return_var = 'BL_08_CHECK_FAILED'
            except KeyError as e:
                print(f"{e}\n'BL_08_CHECK_FAILED'\nNo modern value found: {modern}\n")
                return_var = 'BL_08_CHECK_FAILED'

        return return_var

    def bl09(self):
        """
        B.L.09 Function - Border Bridge Inspection Responsibility
        """
        historic = self.historic_data["OTHER_STATE_PCNT_098B"].iloc[0]
        modern = float(self.brdr_brg_pct_resp) if self.brdr_brg_pct_resp is not None else None

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_09_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BL_09_CHECK_FAILED'

        return return_var

    def bl10(self, state='Ohio'):
        """
        B.L.10 Function - Border Bridge Designated Lead State
        """
        historic = state_code_conversion(self.historic_data["STATE_CODE_001"].iloc[0])
        modern = state  # //TODO - Determine how to handle this value during transfer

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_10_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\nConversion: "
                  f"{state_code_conversion(self.historic_data['STATE_CODE_001'].iloc[0])}\n")
            return_var = 'BL_10_CHECK_FAILED'

        return return_var

    def bl11(self):
        """
        B.L.11 Function - Bridge Location
        """
        if self.historic_data['LOCATION_009'].iloc[0][0] == "'":
            print('\nB.L.11 - Check entry, \' character included, removing\n')
            historic = self.historic_data['LOCATION_009'].iloc[0].strip("'")
        else:
            historic = self.historic_data['LOCATION_009'].iloc[0]
        modern = self.str_loc

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_11_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BL_11_CHECK_FAILED'

        return return_var

    def bl12(self):
        """
        B.L.12 Function - Metropolitan Planning Organization

        Previously didn't exist
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_12_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\nConversion: "
                  f"{state_code_conversion(self.historic_data['STATE_CODE_001'].iloc[0])}\n")
            return_var = 'BL_12_CHECK_FAILED'

        return return_var

    def bcl01(self):
        """
        B.CL.01 Function - Owner
        """
        historic = self.historic_data['OWNER_022'].iloc[0]
        modern = self.maintenance_authority

        if historic == modern:
            return_var = None
        else:
            print(f"BCL_01_CHECK_FAILED\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BCL_01_CHECK_FAILED'

        return return_var

    def bcl02(self):
        """
        B.CL.02 Function - Maintenance Responsibility
        """
        historic = self.historic_data['MAINTENANCE_021'].iloc[0]
        modern = self.maintenance_authority

        if historic == modern:
            return_var = None
        else:
            print(f"'BCL_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BCL_02_CHECK_FAILED'

        return return_var

    def bcl03(self):
        """
        B.CL.03 Function - Federal or Tribal Land Access
        """
        historic = self.historic_data['FEDERAL_LANDS_105'].iloc[0]
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'BCL_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BCL_03_CHECK_FAILED'

        return return_var

    def bcl04(self):
        """
        B.CL.04 Function - Historic Significance
        """
        historic = self.historic_data['HISTORY_037'].iloc[0]
        modern = float(self.hist_sgn_cd)

        if historic == modern:
            return_var = None
        else:
            print(f"'BCL_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BCL_04_CHECK_FAILED'

        return return_var

    def bcl05(self):
        """
        B.CL.05 Function - Toll
        """
        historic = self.historic_data['TOLL_020'].iloc[0]
        modern = float(self.toll_cd)

        if historic == modern:
            return_var = None
        else:
            print(f"'BCL_05_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BCL_05_CHECK_FAILED'

        return return_var

    def bcl06(self):
        """
        B.CL.06 Function - Federal or Tribal Land Access
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'BCL_06_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BCL_06_CHECK_FAILED'

        return return_var

    def bsp01(self):  # Multiple field check example
        """
        B.SP.01 Function - Span Configuration Designation
        """
        historic = {
            '1': self.historic_data['STRUCTURE_KIND_043A'].iloc[0],
            '2': self.historic_data['STRUCTURE_TYPE_043B'].iloc[0],
            '3': self.historic_data['APPR_KIND_044A'].iloc[0],
            '4': self.historic_data['APPR_TYPE_044B'].iloc[0],
        }
        modern = {
            '1': float(self.main_str_mtl_cd),
            '2': float(self.main_str_type_cd),
            '3': float(self.apprh_str_mtl_cd),
            '4': float(self.apprh_str_type_cd),
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.SP_01_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.SP_01_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bsp02(self):
        """
        B.SP.02 Function - Number of Spans
        """
        historic = {
            '1': self.historic_data['MAIN_UNIT_SPANS_045'].iloc[0],
            '2': self.historic_data['APPR_SPANS_046'].iloc[0],
        }
        modern = {
            '1': float(self.main_spans),
            '2': float(self.apprh_spans),
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.SP_02_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.SP_02_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bsp03(self):
        """
        B.SP.03 Function - Number of Beam Lines
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'BSP_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'BSP_03_CHECK_FAILED'

        return return_var

    def bsp04(self):
        """
        B.SP.04 Function - Span Material
        """
        historic = {
            '1': self.historic_data['STRUCTURE_KIND_043A'].iloc[0],
            '2': self.historic_data['APPR_KIND_044A'].iloc[0],
        }
        modern = {
            '1': float(self.main_str_mtl_cd),
            '2': float(self.apprh_str_mtl_cd),
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.SP_04_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.SP_04_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bsp05(self):
        """
        B.SP.05 Function - Span Configuration Designation
        """
        historic = {
            '1': self.historic_data['STRUCTURE_KIND_043A'].iloc[0],
            '2': self.historic_data['STRUCTURE_TYPE_043B'].iloc[0],
            '3': self.historic_data['APPR_KIND_044A'].iloc[0],
            '4': self.historic_data['APPR_TYPE_044B'].iloc[0],
        }
        modern = {
            '1': float(self.main_str_mtl_cd),
            '2': float(self.main_str_type_cd),
            '3': float(self.apprh_str_mtl_cd),
            '4': float(self.apprh_str_type_cd),
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.SP_05_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.SP_05_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bsp06(self):
        """
        B.SP.06 Function - Span Type
        """
        historic = {
            '1': self.historic_data['STRUCTURE_TYPE_043B'].iloc[0],
            '2': self.historic_data['APPR_TYPE_044B'].iloc[0],
        }
        modern = {
            '1': float(self.main_str_type_cd),
            '2': float(self.apprh_str_type_cd),
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.SP_06_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.SP_06_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bsp07(self):
        """
        B.SP.07 Function - Span Protective System
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SP_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SP_07_CHECK_FAILED'

        return return_var

    def bsp08(self):
        """
        B.SP.08 Function - Deck Interaction
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SP_08_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SP_08_CHECK_FAILED'

        return return_var

    def bsp09(self):
        """
        B.SP.09 Function - Deck Material and Type
        """
        historic = self.historic_data['DECK_STRUCTURE_TYPE_107'].iloc[0]
        modern = self.deck_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SP_09_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SP_09_CHECK_FAILED'

        return return_var

    def bsp10(self):
        """
        B.SP.10 Function - Wearing Surface
        """
        historic = self.historic_data['SURFACE_TYPE_108A'].iloc[0]
        modern = self.wearing_surf_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SP_10_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SP_10_CHECK_FAILED'

        return return_var

    def bsp11(self):
        """
        B.SP.11 Function - Deck Protective System
        """
        historic = self.historic_data['MEMBRANE_TYPE_108B'].iloc[0]
        modern = self.deck_prot_extl_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SP_11_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SP_11_CHECK_FAILED'

        return return_var

    def bsp12(self):
        """
        B.SP.12 Function - Deck Reinforcing Protective System
        """
        historic = self.historic_data['DECK_PROTECTION_108C'].iloc[0]
        modern = self.deck_prot_int_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SP_12_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SP_12_CHECK_FAILED'

        return return_var

    def bsp13(self):
        """
        B.SP.13 Function - Deck Stay-In-Place Forms
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SP_13_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SP_13_CHECK_FAILED'

        return return_var

    def bsb01(self):
        """
        B.SB.01 Function - Substructure Configuration Designation
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SB_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SB_01_CHECK_FAILED'

        return return_var

    def bsb02(self):
        """
        B.SB.02 Function - Number of Substructure Units
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SB_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SB_02_CHECK_FAILED'

        return return_var

    def bsb03(self):
        """
        B.SB.03 Function - Substructure Material
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SB_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SB_03_CHECK_FAILED'

        return return_var

    def bsb04(self):
        """
        B.SB.01 Function - Substructure Configuration Designation
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SB_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SB_01_CHECK_FAILED'

        return return_var

    def bsb05(self):
        """
        B.SB.01 Function - Substructure Configuration Designation
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SB_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SB_01_CHECK_FAILED'

        return return_var

    def bsb06(self):
        """
        B.SB.01 Function - Substructure Configuration Designation
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SB_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SB_01_CHECK_FAILED'

        return return_var

    def bsb07(self):
        """
        B.SB.01 Function - Substructure Configuration Designation
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.SB_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.SB_01_CHECK_FAILED'

        return return_var

    def brh01(self):
        """
        B.RH.01 - Bridge Railings
        """
        historic = self.historic_data['RAILINGS_036A'].iloc[0]
        modern = self.survey_railing

        if historic == modern:
            return_var = None
        else:
            print(f"'B.RH_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.RH_01_CHECK_FAILED'

        return return_var

    def brh02(self):
        """
        B.RH.02 - Transitions
        """
        historic = self.historic_data['TRANSITIONS_036B'].iloc[0]
        modern = self.survey_transition

        if historic == modern:
            return_var = None
        else:
            print(f"'B.RH_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.RH_02_CHECK_FAILED'

        return return_var

    def bg01(self):
        """
        B.G.01 - NBIS Bridge Length
        """
        historic = self.historic_data['STRUCTURE_LEN_MT_049'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.ovrl_str_len

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_01_CHECK_FAILED'

        return return_var

    def bg02(self):
        """
        B.G.02 - Total Bridge Length
        """
        historic = self.historic_data['STRUCTURE_LEN_MT_049'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.ovrl_str_len

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_02_CHECK_FAILED'

        return return_var

    def bg03(self):
        """
        B.G.03 - Maximum Span Length
        """
        historic = self.historic_data['STRUCTURE_LEN_MT_049'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.max_span_len

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_03_CHECK_FAILED'

        return return_var

    def bg04(self):
        """
        B.G.04 - Minimum Span Length

        //TODO - This one doesn't make much sense, same as maximum
        """
        historic = self.historic_data['MAX_SPAN_LEN_MT_048'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.max_span_len

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_01_CHECK_FAILED'

        return return_var

    def bg05(self):
        """
        B.G.05 - Bridge Width Out-to-Out
        """
        historic = self.historic_data['DECK_WIDTH_MT_052'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.deck_wd

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_05_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_05_CHECK_FAILED'

        return return_var

    def bg06(self):
        """
        B.G.06 - Bridge Width Curb-to-Curb
        """
        historic = self.historic_data['ROADWAY_WIDTH_MT_051'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.brg_rdw_wd

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_06_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_06_CHECK_FAILED'

        return return_var

    def bg07(self):
        """
        B.G.07 - Left Curb or Sidewalk Width
        """
        historic = self.historic_data['LEFT_CURB_MT_050A'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.sidw_wd_l

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_07_CHECK_FAILED'

        return return_var

    def bg08(self):
        """
        B.G.08 - Right Curb or Sidewalk Width
        """
        historic = self.historic_data['RIGHT_CURB_MT_050B'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.sidw_wd_r

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_01_CHECK_FAILED'

        return return_var

    def bg09(self):
        """
        B.G.09 - Approach Roadway Width
        """
        historic = self.historic_data['APPR_WIDTH_MT_032'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.apprh_rdw_wd

        if historic - modern < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_09_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_09_CHECK_FAILED'

        return return_var

    def bg10(self):
        """
        B.G.10 - Bridge Median
        """
        historic = self.historic_data['MEDIAN_CODE_033'].iloc[0]
        historic_units = historic * units['meter']
        modern_units = historic_units.to('feet')
        historic = float(modern_units.magnitude)  # drops units after conversion for comparison

        modern = self.median_cd

        if historic - float(modern) < 1:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_10_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_10_CHECK_FAILED'

        return return_var

    def bg11(self):
        """
        B.G.11 - NBIS Bridge Length
        """
        historic = self.historic_data['DEGREES_SKEW_034'].iloc[0]
        modern = self.skew_deg

        if historic == modern:
            return_var = None
        else:
            print(f"'B.G_11_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_11_CHECK_FAILED'

        return return_var

    def bg12(self):
        """
        B.G.12 - Curved Bridge
        """
        historic = ''
        modern = ''

        if historic == modern:  # 1' margin of error on conversion
            return_var = None
        else:
            print(f"'B.G_12_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_12_CHECK_FAILED'

        return return_var

    def bg13(self):
        """
        B.G.13 - Maximum Bridge Height
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.G_13_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_13_CHECK_FAILED'

        return return_var

    def bg14(self):
        """
        B.G.14 - Sidehill Bridge
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.G_14_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_14_CHECK_FAILED'

        return return_var

    def bg15(self):
        """
        B.G.15 - Irregular Deck Area
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.G_15_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_15_CHECK_FAILED'

        return return_var

    def bg16(self):
        """
        B.G.16 - Calculated Deck Area
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.G_16_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.G_16_CHECK_FAILED'

        return return_var

    def bf01(self):
        """
        B.F.01 Function - Feature Type
        """
        historic = {
            '1': self.historic_data['SERVICE_ON_042A'].iloc[0],
            '2': self.historic_data['SERVICE_UND_042B'].iloc[0],
        }
        modern = {
            '1': float(self.type_serv1_cd),
            '2': float(self.type_serv2_cd),
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.F_01_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.F_01_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bf02(self):
        """
        B.F.02 Function - Feature Location
        """
        historic = {
            '1': self.historic_data['SERVICE_ON_042A'].iloc[0],
            '2': self.historic_data['SERVICE_UND_042B'].iloc[0],
        }
        modern = {
            '1': float(self.type_serv1_cd),
            '2': float(self.type_serv2_cd),
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.F_02_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.F_02_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bf03(self):
        """
        B.F.03 Function - Feature Name
        """
        historic = {
            '1': self.historic_data['FEATURES_DESC_006A'].iloc[0],
            '2': self.historic_data['FACILITY_CARRIED_007'].iloc[0],
        }
        modern = {
            '1': self.invent_feat,
            '2': self.str_loc_carried,
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.F_03_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.F_03_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def brt01(self):
        """
        B.RT.01 - Route Designation
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.RT_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.RT_01_CHECK_FAILED'

        return return_var

    def brt02(self):
        """
        B.RT.02 - Route Number
        """
        historic = {
            '1': self.historic_data['ROUTE_NUMBER_005D'].iloc[0],
            '2': self.historic_data['DIRECTION_005E'].iloc[0],
        }
        modern = {
            '1': '',
            '2': self.str_loc_carried,
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.RT_02_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.RT_02_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def brt03(self):
        """
        B.RT.03 - Route direction
        """
        historic = self.historic_data['TRAFFIC_DIRECTION_102'].iloc[0]
        modern = self.dir_traffic_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.RT_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.RT_03_CHECK_FAILED'

        return return_var

    def brt04(self):
        """
        B.RT.04 - Route Type
        """
        historic = self.historic_data['ROUTE_PREFIX_005B'].iloc[0]
        modern = self.invent_hwy_sys_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.RT_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.RT_04_CHECK_FAILED'

        return return_var

    def brt05(self):
        """
        B.RT.05 - Service Type
        """
        historic = self.historic_data['SERVICE_LEVEL_005C'].iloc[0]
        modern = self.invent_hwy_dsgt_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.RT_05_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.RT_05_CHECK_FAILED'

        return return_var

    def bh01(self):
        """
        B.H.01 - Functional Classification
        """
        historic = self.historic_data['FUNCTIONAL_CLASS_026'].iloc[0]
        modern = self.func_clas_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_01_CHECK_FAILED'

        return return_var

    def bh02(self):
        """
        B.H.02 - Functional Classification
        """
        historic = self.historic_data['FUNCTIONAL_CLASS_026'].iloc[0]
        modern = self.func_clas_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_02_CHECK_FAILED'

        return return_var

    def bh03(self):
        """
        B.H.03 - NHS Designation
        """
        historic = self.historic_data['HIGHWAY_SYSTEM_104'].iloc[0]
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_03_CHECK_FAILED'

        return return_var

    def bh04(self):
        """
        B.H.04 - National Highway Freight Network
        """
        historic = self.historic_data['NATIONAL_NETWORK_110'].iloc[0]
        modern = self.dsgt_natl_netw_sw

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_04_CHECK_FAILED'

        return return_var

    def bh05(self):
        """
        B.H.05 - Functional Classification
        """
        historic = self.historic_data['STRAHNET_HIGHWAY_100'].iloc[0]
        modern = self.dfns_hwy_dsgt_sw

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_05_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_05_CHECK_FAILED'

        return return_var

    def bh06(self):
        """
        B.H.06 - LRS Route ID
        """
        historic = {
            '1': self.historic_data['LRS_INV_ROUTE_013A'].iloc[0],
            '2': self.historic_data['SUBROUTE_NO_013B'].iloc[0],
        }
        modern = {
            '1': '',
            '2': '',
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.H_06_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.H_06_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bh07(self):
        """
        B.H.07 - LRS Mile Point
        """
        historic = self.historic_data['KILOPOINT_011'].iloc[0]
        modern = self.func_clas_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_07_CHECK_FAILED'

        return return_var

    def bh08(self):
        """
        B.H.08 - Lanes on Highway
        """
        historic = self.historic_data['TRAFFIC_LANES_ON_028A'].iloc[0]
        modern = self.lanes_on

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_08_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_08_CHECK_FAILED'

        return return_var

    def bh09(self):
        """
        B.H.09 - Annual Average Daily Traffic
        """
        historic = self.historic_data['ADT_029'].iloc[0]
        modern = self.invent_rte_adt

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_09_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_09_CHECK_FAILED'

        return return_var

    def bh10(self):
        """
        B.H.10 - Annual Average Daily Truck Traffic
        """
        historic = self.historic_data['PERCENT_ADT_TRUCK_109'].iloc[0]
        modern = self.func_clas_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_10_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_10_CHECK_FAILED'

        return return_var

    def bh11(self):
        """
        B.H.11 - Year of Annual Average Daily Traffic
        """
        historic = self.historic_data['YEAR_ADT_030'].iloc[0]
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_11_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_11_CHECK_FAILED'

        return return_var

    def bh12(self):
        """
        B.H.12 - Highway Maximum Usable Vertical Clearance
        """
        historic = self.historic_data['MIN_VERT_CLR_010'].iloc[0]
        modern = self.func_clas_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_12_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_12_CHECK_FAILED'

        return return_var

    def bh13(self):
        """
        B.H.13 - Highway Minimum Vertical Clearance
        """
        historic = {
            '1': self.historic_data['VERT_CLR_UND_REF_054A'].iloc[0],
            '2': self.historic_data['VERT_CLR_UND_054B'].iloc[0],
        }
        modern = {
            '1': self.minvrt_undclr_c,
            '2': '',
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.H_13_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.H_13_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bh14(self):
        """
        B.H.14 - Highway Minimum Horizontal Clearance, Left
        """
        historic = {
            '1': self.historic_data['LAT_UND_REF_055A'].iloc[0],
            '2': self.historic_data['LEFT_LAT_UND_MT_056'].iloc[0],
        }
        modern = {
            '1': self.minvrt_undclr_c,
            '2': '',
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.H_13_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.H_13_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bh15(self):
        """
        B.H.15 - Highway Minimum Horizontal Clearance, Right
        """
        historic = {
            '1': self.historic_data['LAT_UND_REF_055A'].iloc[0],
            '2': self.historic_data['LAT_UND_MT_055B'].iloc[0],
        }
        modern = {
            '1': '',
            '2': '',
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.H_15_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.H_15_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bh16(self):
        """
        B.H.16 - Highway Maximum Usable Surface Width
        """
        historic = self.historic_data['HORR_CLR_MT_047'].iloc[0]
        modern = self.min_horiz_clr_c

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_16_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_16_CHECK_FAILED'

        return return_var

    def bh17(self):
        """
        B.H.17 - Bypass Detour Length
        """
        historic = self.historic_data['DETOUR_KILOS_019'].iloc[0]
        modern = self.bypass_len

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_17_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_17_CHECK_FAILED'

        return return_var

    def bh18(self):
        """
        B.H.18 - Crossing Bridge Number
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.H_18_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.H_18_CHECK_FAILED'

        return return_var

    def brr01(self):
        """
        B.RR.01 - Railroad Service Type
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.RR_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.RR_01_CHECK_FAILED'

        return return_var

    def brr02(self):
        """
        B.RR.02 - Railroad Minimum Vertical Clearance
        """
        historic = {
            '1': self.historic_data['VERT_CLR_UND_REF_054A'].iloc[0],
            '2': self.historic_data['VERT_CLR_UND_054B'].iloc[0],
        }
        modern = {
            '1': '',
            '2': '',
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.RR_02_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.RR_02_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def brr03(self):
        """
        B.RR.03 - Railroad Minimum Horizontal Offset
        """
        historic = {
            '1': self.historic_data['VERT_CLR_UND_REF_054A'].iloc[0],
            '2': self.historic_data['VERT_CLR_UND_054B'].iloc[0],
        }
        modern = {
            '1': '',
            '2': '',
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.RR_03_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.RR_03_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bn01(self):
        """
        B.N.01 - Navigable Waterway
        """
        historic = self.historic_data['NAVIGATION_038'].iloc[0]
        modern = self.nav_control_sw

        if historic == modern:
            return_var = None
        else:
            print(f"'B.N_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.N_01_CHECK_FAILED'

        return return_var

    def bn02(self):
        """
        B.N.02 - Navigation Minimum Vertical Clearance
        """
        historic = {
            '1': self.historic_data['NAV_VERT_CLR_MT_039'].iloc[0],
            '2': self.historic_data['STRUCTURE_TYPE_043B'].iloc[0],
            '3': self.historic_data['MIN_NAV_CLR_MT_116'].iloc[0]
        }
        modern = {
            '1': self.nav_vrt_clr,
            '2': self.main_str_type_cd,
            '3': self.min_nav_vrt_clr
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.N_02_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.N_02_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bn03(self):
        """
        B.N.03 - Movable Bridge Maximum Navigation Vertical Clearance
        """
        historic = {
            '1': self.historic_data['NAV_VERT_CLR_MT_039'].iloc[0],
            '2': self.historic_data['STRUCTURE_TYPE_043B'].iloc[0],
            '3': self.historic_data['MIN_NAV_CLR_MT_116'].iloc[0]
        }
        modern = {
            '1': self.nav_vrt_clr,
            '2': self.main_str_type_cd,
            '3': ''
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.N_03_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.N_03_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bn04(self):
        """
        B.N.04 - Navigation Channel Width
        """
        historic = self.historic_data['NAV_HORR_CLR_MT_040'].iloc[0]
        modern = self.nav_horiz_clr

        if historic == modern:
            return_var = None
        else:
            print(f"'B.N_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.N_04_CHECK_FAILED'

        return return_var

    def bn05(self):
        """
        B.N.05 - Navigation Horizontal Clearance
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.N_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.N_01_CHECK_FAILED'

        return return_var

    def bn06(self):
        """
        B.N.06 - Substructure Navigation Protection
        """
        historic = self.historic_data['PIER_PROTECTION_111'].iloc[0]
        modern = self.subs_fenders

        if historic == modern:
            return_var = None
        else:
            print(f"'B.N_06_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.N_06_CHECK_FAILED'

        return return_var

    def blr01(self):
        """
        B.LR.01 - Design Load
        """

        historic = self.historic_data['DESIGN_LOAD_031'].iloc[0]
        modern = self.design_load_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_01_CHECK_FAILED'

        return return_var

    def blr02(self):
        """
        B.LR.02 - Design Method
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_02_CHECK_FAILED'

        return return_var

    def blr03(self):
        """
        B.LR.03 - Load Rating Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_03_CHECK_FAILED'

        return return_var

    def blr04(self):
        """
        B.LR.04 - Load Rating Date
        """
        historic = self.historic_data['OPR_RATING_METH_063'].iloc[0]
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_04_CHECK_FAILED'

        return return_var

    def blr05(self):
        """
        B.LR.05 - Load Rating Date
        """
        historic = self.historic_data['INVENTORY_RATING_066'].iloc[0]
        modern = self.rat_inv_load_fact

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_05_CHECK_FAILED'

        return return_var

    def blr06(self):
        """
        B.LR.06 - Operating Load Rating Factor
        """
        historic = self.historic_data['OPERATING_RATING_064'].iloc[0]
        modern = self.rat_opr_load_fact

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_06_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_06_CHECK_FAILED'

        return return_var

    def blr07(self):
        """
        B.LR.07 - Controlling Legal Load Rating Factor
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_07_CHECK_FAILED'

        return return_var

    def blr08(self):
        """
        B.LR.08 - Routine Permit Loads
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.LR_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.LR_03_CHECK_FAILED'

        return return_var

    def bps01(self):
        """
        B.PS.01 - Load Posting Status
        """
        historic = self.historic_data['OPEN_CLOSED_POSTED_041'].iloc[0]
        modern = self.gen_opr_status

        if historic == modern:
            return_var = None
        else:
            print(f"'B.PS_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.PS_01_CHECK_FAILED'

        return return_var

    def bps02(self):
        """
        B.PS.02 - Posting Status Change Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.PS_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.PS_02_CHECK_FAILED'

        return return_var

    def bep01(self):
        """
        B.EP.01 - Legal Load Configuration
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.EP_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.EP_01_CHECK_FAILED'

        return return_var

    def bep02(self):
        """
        B.EP.02 - Legal Load Rating Factor
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.EP_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.EP_02_CHECK_FAILED'

        return return_var

    def bep03(self):
        """
        B.EP.03 - Posting Type
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.EP_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.EP_03_CHECK_FAILED'

        return return_var

    def bep04(self):
        """
        B.EP.04 - Posting Value
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.EP_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.EP_04_CHECK_FAILED'

        return return_var

    def bir01(self):
        """
        B.IR.01 - NSTM Inspection Required
        """
        historic = self.historic_data['FRACTURE_092A'].iloc[0]
        modern = self.frac_crit_insp_sw

        if historic == modern:
            return_var = None
        else:
            print(f"'B.EP_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IR_01_CHECK_FAILED'

        return return_var

    def bir02(self):
        """
        B.IR.02 - Fatigue Details
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IR_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IR_02_CHECK_FAILED'

        return return_var

    def bir03(self):
        """
        B.IR.03 - Underwater Inspection Required
        """
        historic = self.historic_data['UNDWATER_LOOK_SEE_092B'].iloc[0]
        modern = self.dive_insp_sw

        if historic == modern:
            return_var = None
        else:
            print(f"'B.EP_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.EP_03_CHECK_FAILED'

        return return_var

    def bir04(self):
        """
        B.IR.04 - NSTM Inspection Required
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.EP_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.EP_04_CHECK_FAILED'

        return return_var

    def bie01(self):
        """
        B.IE.01 - Inspection Type
        """
        historic = {
            '1': self.historic_data['DATE_OF_INSPECT_090'].iloc[0],
            '2': self.historic_data['FRACTURE_092A'].iloc[0],
            '3': self.historic_data['FRACTURE_LAST_DATE_093A'].iloc[0],
            '4': self.historic_data['UNDWATER_LOOK_SEE_092B'].iloc[0],
            '5': self.historic_data['UNDWATER_LAST_DATE_093B'].iloc[0],
            '6': self.historic_data['SPEC_INSPECT_092C'].iloc[0],
            '7': self.historic_data['SPEC_LAST_DATE_093C'].iloc[0]
        }
        modern = {
            '1': self.insp_dt,
            '2': self.frac_crit_insp_sw,
            '3': self.frac_crit_insp_dt,
            '4': self.dive_insp_sw,
            '5': self.dive_insp_dt,
            '6': self.spcl_insp_sw,
            '7': self.spcl_insp_dt
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.IE_01_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.IE_01_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bie02(self):
        """
        B.IE.02 - Inspection Begin Date
        """
        historic = {
            '1': self.historic_data['DATE_OF_INSPECT_090'].iloc[0],
            '2': self.historic_data['FRACTURE_LAST_DATE_093A'].iloc[0],
            '3': self.historic_data['UNDWATER_LAST_DATE_093B'].iloc[0],
            '4': self.historic_data['UNDWATER_LOOK_SEE_092B'].iloc[0],
            '5': self.historic_data['UNDWATER_LAST_DATE_093B'].iloc[0],
            '6': self.historic_data['SPEC_INSPECT_092C'].iloc[0],
            '7': self.historic_data['SPEC_LAST_DATE_093C'].iloc[0]
        }
        modern = {
            '1': self.insp_dt,
            '2': self.frac_crit_insp_sw,
            '3': self.frac_crit_insp_dt,
            '4': self.dive_insp_sw,
            '5': self.dive_insp_dt,
            '6': self.spcl_insp_sw,
            '7': self.spcl_insp_dt
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.IE_01_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.IE_01_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bie03(self):
        """
        B.IE.03 - Inspection Completion Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_03_CHECK_FAILED'

        return return_var

    def bie04(self):
        """
        B.IE.04 - Nationally Certified Bridge Inspector
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_03_CHECK_FAILED'

        return return_var

    def bie05(self):
        """
        B.IE.05 - Inspection Interval
        """
        historic = {
            '1': self.historic_data['INSPECT_FREQ_MONTHS_091'].iloc[0],
            '2': self.historic_data['FRACTURE_092A'].iloc[0],
            '3': self.historic_data['UNDWATER_LOOK_SEE_092B'].iloc[0],
            '4': self.historic_data['SPEC_INSPECT_092C'].iloc[0]
        }
        modern = {
            '1': self.dsgt_insp_freq,
            '2': self.frac_crit_insp_sw,
            '3': self.frac_crit_insp_dt,
            '4': self.frac_crit_insp_dt
        }

        temp_dict = {}

        for key, value in historic.items():
            if historic[key] == modern[key]:
                temp_dict[key] = None
            else:
                print(f"B.IE_05_CHECK_{key}_FAILED\n\nExpected the values:\nHistoric: {historic[key]}\n"
                      f"Modern: {modern[key]}\nto be equal\n\n\n")
                temp_dict[key] = f"B.IE_05_CHECK_{key}_FAILED"

        return_var = temp_dict

        return return_var

    def bie06(self):
        """
        B.IE.06 - Inspection Due Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_06_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_06_CHECK_FAILED'

        return return_var

    def bie07(self):
        """
        B.IE.07 - Risk-Based Inspection Interval Method
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_07_CHECK_FAILED'

        return return_var

    def bie08(self):
        """
        B.IE.08 - Inspection Quality Control Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_08_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_08_CHECK_FAILED'

        return return_var

    def bie09(self):
        """
        B.IE.09 - Inspection Quality Assurance Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_09_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_09_CHECK_FAILED'

        return return_var

    def bie10(self):
        """
        B.IE.10 - Inspection Completion Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_10_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_10_CHECK_FAILED'

        return return_var

    def bie11(self):
        """
        B.IE.11 - Inspection Note
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_11_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_11_CHECK_FAILED'

        return return_var

    def bie12(self):
        """
        B.IE.12 - Inspection Equipment
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_07_CHECK_FAILED'

        return return_var

    def bc01(self):
        """
        B.C.01 - Deck Condition Rating
        """
        historic = self.historic_data['DECK_COND_058'].iloc[0]
        modern = self.deck_summary

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_01_Deck_Condition_Rating'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_01_CHECK_FAILED'

        return return_var

    def bc02(self):
        """
        B.C.02 - Superstructure Condition Rating
        """
        historic = self.historic_data['SUPERSTRUCTURE_COND_059'].iloc[0]
        modern = self.sups_summary

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_02_CHECK_FAILED'

        return return_var

    def bc03(self):
        """
        B.C.03 - Substructure Condition Rating
        """
        historic = self.historic_data['SUBSTRUCTURE_COND_060'].iloc[0]
        modern = self.subs_summary

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_03_CHECK_FAILED'

        return return_var

    def bc04(self):
        """
        B.C.04 - Culvert Condition Rating
        """
        historic = self.historic_data['CULVERT_COND_062'].iloc[0]
        modern = self.culvert_summary

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_04_CHECK_FAILED'

        return return_var

    def bc05(self):
        """
        B.C.05 - Bridge Railing Condition Rating
        """
        historic = self.historic_data['RAILINGS_036A'].iloc[0]
        modern = self.survey_railing

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_05_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_05_CHECK_FAILED'

        return return_var

    def bc06(self):
        """
        B.C.06 - Inspection Completion Date
        """
        historic = self.historic_data['TRANSITIONS_036B'].iloc[0]
        modern = self.survey_transition

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_06_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_06_CHECK_FAILED'

        return return_var

    def bc07(self):
        """
        B.C.07 - Bridge Bearings Condition Rating
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_07_CHECK_FAILED'

        return return_var

    def bc08(self):
        """
        B.C.08 - Bridge Joints Condition Rating
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_08_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_08_CHECK_FAILED'

        return return_var

    def bc09(self):
        """
        B.C.09 - Channel Condition Rating
        """
        historic = self.historic_data['CHANNEL_COND_061'].iloc[0]
        modern = self.chan_summary

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_09_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_09_CHECK_FAILED'

        return return_var

    def bc10(self):
        """
        B.C.10 - Channel Protection Condition Rating
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_10_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_10_CHECK_FAILED'

        return return_var

    def bc11(self):
        """
        B.C.11 - Scour Condition Rating
        """
        historic = self.historic_data['SCOUR_CRITICAL_113'].iloc[0]
        modern = self.scour_crit_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_11_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_11_CHECK_FAILED'

        return return_var

    def bc12(self):
        """
        B.C.12 - Bridge Condition Classification
        """
        historic = self.historic_data['BRIDGE_CONDITION'].iloc[0]
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_12_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_12_CHECK_FAILED'

        return return_var

    def bc13(self):
        """
        B.C.13 - Lowest Condition Rating Code
        """
        historic = self.historic_data['LOWEST_RATING'].iloc[0]
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_13_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_13_CHECK_FAILED'

        return return_var

    def bc14(self):
        """
        B.C.14 - Underwater Inspection Condition
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_14_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_14_CHECK_FAILED'

        return return_var

    def bc15(self):
        """
        B.C.15 - Underwater Inspection Condition
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_15_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.C_15_CHECK_FAILED'

        return return_var

    def bap01(self):
        """
        B.AP.01 - Approach Roadway Alignment
        """
        historic = self.historic_data['APPR_ROAD_EVAL_072'].iloc[0]
        modern = self.apprh_algn_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.AP_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.AP_01_CHECK_FAILED'

        return return_var

    def bap02(self):
        """
        B.AP.02 - Inspection Completion Date
        """
        historic = self.historic_data['WATERWAY_EVAL_071'].iloc[0]
        modern = self.ww_adequacy_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.AP_02_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.AP_02_CHECK_FAILED'

        return return_var

    def bap03(self):
        """
        B.AP.03 - Scour Vulnerability
        """
        historic = self.historic_data['SCOUR_CRITICAL_113'].iloc[0]
        modern = self.scour_crit_cd

        if historic == modern:
            return_var = None
        else:
            print(f"'B.AP_03_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.AP_03_CHECK_FAILED'

        return return_var

    def bap04(self):
        """
        B.AP.04 - Scour Plan of Action
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.AP_04_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.AP_04_CHECK_FAILED'

        return return_var

    def bap05(self):
        """
        B.AP.05 - Seismic Vulnerability
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.AP_05_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.AP_05_CHECK_FAILED'

        return return_var

    def bw01(self):
        """
        B.W.01 - Year Built
        """
        historic = self.historic_data['YEAR_BUILT_027'].iloc[0]
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.W_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.W_01_CHECK_FAILED'

        return return_var

    def bw02(self):
        """
        B.W.02 - Year Work Performed
        """
        historic = self.historic_data['YEAR_RECONSTRUCTED_106'].iloc[0]
        modern = self.maj_recon_dt

        if historic == modern:
            return_var = None
        else:
            print(f"'B.C_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.W_02_CHECK_FAILED'

        return return_var

    def bw03(self):
        """
        B.C.01 - Inspection Completion Date
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.IE_07_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\n")
            return_var = 'B.IE_07_CHECK_FAILED'

        return return_var


if __name__ == "__main__":
    if type(sys.argv[1]) == list():
        for entry in sys.argv[1]:
            SNBITransfer(entry)
    else:
        SNBITransfer(sys.argv[1])
