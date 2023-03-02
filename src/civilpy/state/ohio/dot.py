import io
import os
import re
import folium
import pandas as pd
from bs4 import BeautifulSoup
import json
from collections import OrderedDict
import requests


def help_function():
    """
    To use the dicts, import them into python, and then use the two-letter code to get the translations, i.e.
    basemap_labels['BA'] will return "Aerial Mapping"

    General Notes:
    General File Naming Format:
        nnnnn(n)_aa###.dgn where:
            nnnnnn - 5 (or 6) digit PID
            aa     - Two-letter code signifying sheet type (see dicts)
            ###    - Three digit number identifying the number of drawings of the same type

    Bridge Design File Naming Format:
        nnnnnn_SFNyyyyyyy_aa###.dgn where:
            nnnnnn   - PID
            yyyyyyy  - 7 digit SFN of the structure
            aa       - Two character bridge plan sheet type
            ###      - Three digit number identifying the number of drawings of the same type

    Culvert Design File Naming Format:
        nnnnnn_CFNyyyyyyy_aa###.dgn where:
            nnnnnn  - PID
            yyyyyyy - 7 digit CFN number of the culvert
            aa      - Two character drainage plan sheet type
            ###     - Three digit number identifying the number of drawings of the same type

    Wall Design File Naming Format:
        nnnnnn_WALLyyy_aa###.dgn where:
            nnnnnn  - PID
            yyy     - Three digit wall number
            aa      - Two digit wall plan sheet type
            ###     - Three digit number identifying the number of drawings of the same type
    """
    print(help(help_function))


basemap_labels = {
    'KB': '3D Model KB',
    'KM': '3D Modeling KM',
    'BC': 'Aerial and Ground Combined',
    'BA': 'Aerial Mapping',
    'BS': 'Bridge',
    'KD': 'Digital Terrain Model',
    'BD': 'Drainage',
    'FD': 'Field Digital Terrain Model',
    'BK': 'Geometry',
    'BI': 'Geotechnical',
    'BL': 'Landscaping',
    'BH': 'Lighting',
    'BM': 'MOT',
    'PC': 'Point Cloud',
    'BR': 'Right-of-Way',
    'BP': 'Roadway',
    'BG': 'Signals',
    'KS': 'Superelevation',
    'FB': 'Survey Field Book',
    'BT': 'Traffic Control',
    'BU': 'Utilities',
    'BW': 'Wall'
}

bridge_labels = {
    'SB': 'Bearing',
    'SD': 'Deck Plan',
    'SQ': 'Estimated Quantities',
    'SX': 'Expansion Device Details',
    'SF': 'Forward Abutment',
    'SO': 'Foundation Plan',
    'SN': 'General Notes',
    'SG': 'General Plan',
    'SM': 'Miscellaneous Details',
    'SI': 'Piers',
    'SA': 'Railing',
    'SR': 'Rear Abutment',
    'SL': 'Reinforcing Steel List',
    'SV': 'Removal',
    'SH': 'Sheeting',
    'SP': 'Site Plan',
    'SC': 'Staged Construction Details',
    'SS': 'Superstructure Details',
    'ST': 'Transverse Section'
}

drainage_labels = {
    'XD': 'Channel Cross Sections',
    'DC': 'Culvert Details',
    'DD': 'Details',
    'DE': 'Erosion Control',
    'DM': 'Miscellaneous Details',
    'DN': 'Notes',
    'DP': 'Plan and Profile or Plan',
    'DF': 'Profile',
    'DQ': 'Quantity Table',
    'DB': 'Schematic Plan',
    'DS': 'Sub-Summary'
}

geotechnical_labels = {
    'YL': 'Geohazard Boring Logs',
    'YC': 'Geohazard Cover',
    'YX': 'Geohazard Cross Sections',
    'YD': 'Geohazard Lab Data',
    'YP': 'Geohazard Plan and Profile',
    'YF': 'Geohazard Profile',
    'IC': 'Soil Profile Cover',
    'IX': 'Soil Profile Cross Sections',
    'ID': 'Soil Profile Lad Data',
    'IP': 'Soil Profile, Plan and Profile or Plan',
    'IF': 'Soil Profile, Profile Only',
    'ZL': 'Structure Foundation Exploration Boring Logs',
    'ZC': 'Structure Foundation Exploration Cover',
    'ZD': 'Structure Foundation Exploration Lab Data',
    'ZP': 'Structure Foundation Exploration Plan and Profile',
    'ZF': 'Structure Foundation Exploration Profile'
}

landscaping_labels = {
    'PD': 'Details',
    'PM': 'Miscellaneous Details',
    'PN': 'Notes',
    'PP': 'Plan',
    'PB': 'Schematic Plan',
    'PS': 'Sub-Summary',
}

lighting_labels = {
    'LC': 'Circuit Diagrams',
    'LD': 'Details',
    'LE': 'Elevation Views',
    'LG': 'General Summary',
    'LM': 'Miscellaneous',
    'LN': 'Notes',
    'LP': 'Plan',
    'LQ': 'Quantity Table',
    'LB': 'Schematic Plan',
    'LS': 'Sub-Summary'
}

mot_labels = {
    'XM': 'Cross Sections',
    'MD': 'Detour Plan',
    'MM': 'Miscellaneous',
    'MN': 'Notes',
    'MP': 'Phase Plan and Profile or Plan',
    'MH': 'Phase Details',
    'MF': 'Profile',
    'MQ': 'Quantity Table',
    'MB': 'Schematic Plan',
    'MS': 'Sub-Summary',
    'MY': 'Typical Sections'
}

row_labels = {
    'RC': 'Centerline Plat',
    'RL': 'Legend',
    'RM': 'Property Map',
    'RR': 'Railroad Plat',
    'RB': 'RW Boundary',
    'RD': 'RW Detail',
    'RT': 'RW Topo',
    'RS': 'Summary of Additional RW'
}

roadway_labels = {
    'GC': 'Calculations/Computations',
    'XS': 'Cross Sections',
    'GD': 'Drive Details',
    'GX': 'Fencing Plan',
    'GN': 'General Notes',
    'GG': 'General Summary',
    'XG': 'Grading Plan',
    'GR': 'Guardrail/Barrier Details',
    'GI': 'Intersection/Interchange Details',
    'GJ': 'Maintenance Data',
    'GM': 'Miscellaneous',
    'GA': 'Pavement Details',
    'GP': 'Plan and Profile or Plan',
    'GF': 'Profile',
    'GQ': 'Quantity Table',
    'GB': 'Schematic Plan',
    'GS': 'Sub-Summary',
    'GE': 'Superelevation Table',
    'GT': 'Title Sheet',
    'GY': 'Typical Sections'
}

signal_labels = {
    'CD': 'Details',
    'CG': 'General Summary',
    'CM': 'Miscellaneous',
    'CN': 'Notes',
    'CP': 'Plan',
    'CQ': 'Quantity Table',
    'CS': 'Sub-Summary'
}

traffic_control_labels = {
    'TC': 'Calculations/Computations',
    'TD': 'Details',
    'TE': 'Elevation Views',
    'TN': 'General Notes',
    'TG': 'General Summary',
    'TM': 'Miscellaneous',
    'TP': 'Plan',
    'TQ': 'Quantity Table',
    'TB': 'Schematic Plan',
    'TS': 'Sub-Summary'
}

utility_labels = {
    'UC': 'Calculations/Computations',
    'UD': 'Details',
    'UE': 'Elevation Views',
    'UG': 'General Summary',
    'UM': 'Miscellaneous',
    'UN': 'Notes',
    'UP': 'Plan and Profile or Plan',
    'UF': 'Profile',
    'UQ': 'Quantity Table',
    'UB': 'Schematic Plan',
    'US': 'Sub-Summary'
}

wall_labels = {
    'WC': 'Calculations/Computations',
    'WX': 'Cross Sections',
    'WD': 'Details',
    'WE': 'Elevation',
    'WQ': 'Estimated Quantities',
    'WT': 'Foundation',
    'WM': 'Miscellaneous',
    'WN': 'Notes',
    'WP': 'Plan and Profile or Plan',
    'WF': 'Profile',
    'WB': 'Schematic Plan',
    'WH': 'Sheeting',
    'WL': 'Steel List',
    'WS': 'Sub-Summary',
    'WY': 'Typical Section'
}

all_labels = {
    'basemap_labels': basemap_labels,
    'bridge_labels': bridge_labels,
    'drainage_labels': drainage_labels,
    'geotechnical_labels': geotechnical_labels,
    'landscaping_labels': landscaping_labels,
    'lighting_labels': lighting_labels,
    'mot_labels': mot_labels,
    'row_labels': row_labels,
    'roadway_labels': roadway_labels,
    'signal_labels': signal_labels,
    'traffic_control_labels': traffic_control_labels,
    'utility_labels': utility_labels,
    'wall_labels': wall_labels
}

# These are the 4 regular expressions I built to match our file conventions
gen_file_pattern = re.compile(r"\d{5,6}_\w{2}\d{3}.dgn$")
bridge_file_pattern = re.compile(r"\d{5,6}_SFN\d{7}_\w{2}\d{3}.dgn$")
culvert_file_pattern = re.compile(r"\d{5,6}_CFN\d{7}_\w{2}\d{3}.dgn$")
wall_file_pattern = re.compile(r"\d{5,6}_WALL\d{3}_\w{2}\d{3}.dgn$")


def filter_files_by_category(file_list, label_set):
    """
    Takes a list of files, and determines if any of them contain the labels specific to bridge files from ODOT CADD
    standards.

    :param file_list:
        An unfiltered list of all files to be searched
    :param label_set:
        The category of file you want returned, from the keys in the "all_labels" dictionary above
    :return category_files: a list of files containing relevant category info
    """

    temp_list = []
    category_files = []

    # Builds a list of all files containing the strings in 'bridge labels'
    for file in file_list:
        for label in label_set:
            if label in os.path.basename(file):
                temp_list.append(file)
            else:
                pass

    # Drop "EngData" folder files, generally contains reference files, not project ones
    for file in temp_list:
        if "EngData" not in file:
            category_files.append(file)
        else:
            pass

    return category_files


ohio_counties = {
    "ADAMS": "ADA",
    "ALLEN": "ALL",
    "ASHLAND": "ASD",
    "ASHTABULA": "ATB",
    "ATHENS": "ATH",
    "AUGLAIZE": "AUG",
    "BELMONT": "BEL",
    "BROWN": "BRO",
    "BUTLER": "BUT",
    "CARROLL": "CAR",
    "CHAMPAIGN": "CHP",
    "CLARK": "CLA",
    "CLERMONT": "CLE",
    "CLINTON": "CLI",
    "COLUMBIANA": "COL",
    "COSHOCTON": "COS",
    "CRAWFORD": "CRA",
    "CUYAHOGA": "CUY",
    "DARKE": "DAR",
    "DEFIANCE": "DEF",
    "DELAWARE": "DEL",
    "ERIE": "ERI",
    "FAIRFIELD": "FAI",
    "FAYETTE": "FAY",
    "FRANKLIN": "FRA",
    "FULTON": "FUL",
    "GALLIA": "GAL",
    "GEAUGA": "GEA",
    "GREENE": "GRE",
    "GUERNSEY": "GUE",
    "HAMILTON": "HAM",
    "HANCOCK": "HAN",
    "HARDIN": "HAR",
    "HARRISON": "HAS",
    "HENRY": "HEN",
    "HIGHLAND": "HIG",
    "HOCKING": "HOC",
    "HOLMES": "HOL",
    "HURON": "HUR",
    "JACKSON": "JAC",
    "JEFFERSON": "JEF",
    "KNOX": "KNO",
    "LAKE": "LAK",
    "LAWRENCE": "LAW",
    "LICKING": "LIC",
    "LOGAN": "LOG",
    "LORAIN": "LOR",
    "LUCAS": "LUC",
    "MADISON": "MAD",
    "MAHONING": "MAH",
    "MARION": "MAR",
    "MEDINA": "MED",
    "MEIGS": "MEG",
    "MERCER": "MER",
    "MIAMI": "MIA",
    "MONROE": "MOE",
    "MONTGOMERY": "MOT",
    "MORGAN": "MRG",
    "MORROW": "MRW",
    "MUSKINGUM": "MUS",
    "NOBLE": "NOB",
    "OTTAWA": "OTT",
    "PAULDING": "PAU",
    "PERRY": "PER",
    "PICKAWAY": "PIC",
    "PIKE": "PIK",
    "PORTAGE": "POR",
    "PREBLE": "PRE",
    "PUTNAM": "PUT",
    "RICHLAND": "RIC",
    "ROSS": "ROS",
    "SANDUSKY": "SAN",
    "SCIOTO": "SCI",
    "SENECA": "SEN",
    "SHELBY": "SHE",
    "STARK": "STA",
    "SUMMIT": "SUM",
    "TRUMBULL": "TRU",
    "TUSCARAWAS": "TUS",
    "UNION": "UNI",
    "VAN WERT": "VAN",
    "VINTON": "VIN",
    "WARREN": "WAR",
    "WASHINGTON": "WAS",
    "WAYNE": "WAY",
    "WILLIAMS": "WIL",
    "WOOD": "WOO",
    "WYANDOT": "WYA",
}

NBIS_state_codes = {
    '014': 'Alabama',
    '308': 'Montana',
    '020': 'Alaska',
    '317': 'Nebraska',
    '049': 'Arizona',
    '329': 'Nevada',
    '056': 'Arkansas',
    '331': 'New Hampshire',
    '069': 'Californ',
    '342': 'New Jersey',
    '088': 'Colorado',
    '356': 'New Mexico',
    '091': 'Connecti',
    '362': 'New York',
    '103': 'Delaware',
    '374': 'North Carolina',
    '113': 'District of Columbia',
    '388': 'North Dakota',
    '124': 'Florida',
    '395': 'Ohio',
    '134': 'Georgia',
    '406': 'Oklahoma',
    '159': 'Hawaii',
    '410': 'Oregon',
    '160': 'Idaho',
    '423': 'Pennsylvania',
    '175': 'Illinois',
    '441': 'Rhode Island',
    '185': 'Indiana',
    '454': 'South Carolina',
    '197': 'Iowa',
    '468': 'South Dakota',
    '207': 'Kansas',
    '474': 'Tennessee',
    '214': 'Kentucky',
    '486': 'Texas',
    '226': 'Louisiana',
    '498': 'Utah',
    '231': 'Maine',
    '501': 'Vermont',
    '243': 'Maryland',
    '513': 'Virginia',
    '251': 'Massachusetts',
    '530': 'Washington',
    '265': 'Michigan',
    '543': 'West Virginia',
    '275': 'Minnesota',
    '555': 'Wisconsin',
    '284': 'Mississippi',
    '568': 'Wyoming',
    '297': 'Missouri',
    '721': 'Puerto Rico',
}


def get_bridge_data_from_tims(sfn: str = "6500609"):
    """
    Function to return Bridge data from ODOT TIMS REST server

    :param:
        sfn (str): Bridge structure file number

    :return: A dictionary containing all the values relevant to the desired bridge
    """

    url_1 = f"https://gis.dot.state.oh.us/arcgis/rest/services/TIMS/Assets/MapServer/5/query?where=sfn%3D{sfn}&text=&ob"
    url_2 = "jectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relat"
    url_3 = "ionParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&out"
    url_4 = "SR=&having=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatist"
    url_5 = "ics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resu"
    url_6 = "ltRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&"
    url_7 = "quantizationParameters=&featureEncoding=esriDefault&f=html"

    url = url_1 + url_2 + url_3 + url_4 + url_5 + url_6 + url_7

    s = requests.Session()
    page = s.get(url, timeout=5)
    soup = BeautifulSoup(page.content, 'html5lib')
    s.close()

    bridge_link = soup.find_all('a')

    full_data_url = "https://gis.dot.state.oh.us/" + bridge_link[-1].get('href')
    full_data_url_json = full_data_url + '?f=pjson'

    print(f"\nRetrieving data from url at {full_data_url_json}\n")

    page = s.get(full_data_url_json)
    data_json = json.loads(page.content)
    s.close()

    extracted_data = data_json['feature']['attributes']

    return extracted_data


class TimsBridge:
    """
    General Bridge object to hold data from ODOT TIMS REST SERVER, also contains
    mapping function which can be used in jupyter to determine location
    """

    def __init__(self, sfn):
        print("\nTIMS Bridge Initiated\n")
        self.SFN = sfn

        raw_data = get_bridge_data_from_tims(sfn)

        # This could be replaced with a looped function, but it was breaking IDE autocompletes in an annoying way
        self.objectid = raw_data['OBJECTID']
        self.sfn = raw_data['SFN']
        self.str_loc_carried = raw_data['STR_LOC_CARRIED']
        self.rte_on_brg_cd = raw_data['RTE_ON_BRG_CD']
        self.district = raw_data['DISTRICT']
        self.county_cd = raw_data['COUNTY_CD']
        self.invent_spcl_dsgt = raw_data['INVENT_SPCL_DSGT']
        self.fips_cd = raw_data['FIPS_CD']
        self.invent_on_und_cd = raw_data['INVENT_ON_UND_CD']
        self.invent_hwy_sys_cd = raw_data['INVENT_HWY_SYS_CD']
        self.invent_hwy_dsgt_cd = raw_data['INVENT_HWY_DSGT_CD']
        self.invent_dir_sfx_cd = raw_data['INVENT_DIR_SFX_CD']
        self.invent_feat = raw_data['INVENT_FEAT']
        self.str_loc = raw_data['STR_LOC']
        self.latitude_dd = raw_data['LATITUDE_DD']
        self.longitude_dd = raw_data['LONGITUDE_DD']
        self.brdr_brg_state = raw_data['BRDR_BRG_STATE']
        self.brdr_brg_pct_resp = raw_data['BRDR_BRG_PCT_RESP']
        self.brdr_brg_sfn = raw_data['BRDR_BRG_SFN']
        self.main_str_mtl_cd = raw_data['MAIN_STR_MTL_CD']
        self.main_str_type_cd = raw_data['MAIN_STR_TYPE_CD']
        self.apprh_str_mtl_cd = raw_data['APPRH_STR_MTL_CD']
        self.apprh_str_type_cd = raw_data['APPRH_STR_TYPE_CD']
        self.main_spans = raw_data['MAIN_SPANS']
        self.apprh_spans = raw_data['APPRH_SPANS']
        self.deck_cd = raw_data['DECK_CD']
        self.deck_prot_extl_cd = raw_data['DECK_PROT_EXTL_CD']
        self.deck_prot_int_cd = raw_data['DECK_PROT_INT_CD']
        self.wear_surf_dt = raw_data['WEAR_SURF_DT']
        self.wearing_surf_cd = raw_data['WEARING_SURF_CD']
        self.wearing_surf_thck = raw_data['WEARING_SURF_THCK']
        self.paint_dt = raw_data['PAINT_DT']
        self.yr_built = raw_data['YR_BUILT']
        self.maj_recon_dt = raw_data['MAJ_RECON_DT']
        self.type_serv1_cd = raw_data['TYPE_SERV1_CD']
        self.type_serv2_cd = raw_data['TYPE_SERV2_CD']
        self.lanes_on = raw_data['LANES_ON']
        self.lanes_und = raw_data['LANES_UND']
        self.invent_rte_adt = raw_data['INVENT_RTE_ADT']
        self.bypass_len = raw_data['BYPASS_LEN']
        self.nbis_len_sw = raw_data['NBIS_LEN_SW']
        self.invent_nhs_cd = raw_data['INVENT_NHS_CD']
        self.func_clas_cd = raw_data['FUNC_CLAS_CD']
        self.dfns_hwy_dsgt_sw = raw_data['DFNS_HWY_DSGT_SW']
        self.parallel_str_cd = raw_data['PARALLEL_STR_CD']
        self.dir_traffic_cd = raw_data['DIR_TRAFFIC_CD']
        self.temp_str_sw = raw_data['TEMP_STR_SW']
        self.dsgt_natl_netw_sw = raw_data['DSGT_NATL_NETW_SW']
        self.toll_cd = raw_data['TOLL_CD']
        self.routine_resp_cd = raw_data['ROUTINE_RESP_CD']
        self.routine_resp_cd_2 = raw_data['ROUTINE_RESP_CD_2']
        self.maint_resp_cd = raw_data['MAINT_RESP_CD']
        self.maint_resp_cd_2 = raw_data['MAINT_RESP_CD_2']
        self.insp_resp_cd = raw_data['INSP_RESP_CD']
        self.insp_resp_cd_2 = raw_data['INSP_RESP_CD_2']
        self.hist_sgn_cd = raw_data['HIST_SGN_CD']
        self.nav_control_sw = raw_data['NAV_CONTROL_SW']
        self.nav_vrt_clr = raw_data['NAV_VRT_CLR']
        self.nav_horiz_clr = raw_data['NAV_HORIZ_CLR']
        self.subs_fenders = raw_data['SUBS_FENDERS']
        self.min_nav_vrt_clr = raw_data['MIN_NAV_VRT_CLR']
        self.insp_dt = raw_data['INSP_DT']
        self.dsgt_insp_freq = raw_data['DSGT_INSP_FREQ']
        self.frac_crit_insp_sw = raw_data['FRAC_CRIT_INSP_SW']
        self.fraccrit_insp_freq = raw_data['FRACCRIT_INSP_FREQ']
        self.frac_crit_insp_dt = raw_data['FRAC_CRIT_INSP_DT']
        self.dive_insp_sw = raw_data['DIVE_INSP_SW']
        self.dive_insp_freq = raw_data['DIVE_INSP_FREQ']
        self.dive_insp_dt = raw_data['DIVE_INSP_DT']
        self.spcl_insp_sw = raw_data['SPCL_INSP_SW']
        self.spcl_insp_freq = raw_data['SPCL_INSP_FREQ']
        self.spcl_insp_dt = raw_data['SPCL_INSP_DT']
        self.snooper_insp_sw = raw_data['SNOOPER_INSP_SW']
        self.deck_summary = raw_data['DECK_SUMMARY']
        self.deck_wear_surf = raw_data['DECK_WEAR_SURF']
        self.deck_expn_joints = raw_data['DECK_EXPN_JOINTS']
        self.sups_summary = raw_data['SUPS_SUMMARY']
        self.paint = raw_data['PAINT']
        self.subs_summary = raw_data['SUBS_SUMMARY']
        self.chan_summary = raw_data['CHAN_SUMMARY']
        self.subs_scour = raw_data['SUBS_SCOUR']
        self.culvert_summary = raw_data['CULVERT_SUMMARY']
        self.gen_appraisal = raw_data['GEN_APPRAISAL']
        self.design_load_cd = raw_data['DESIGN_LOAD_CD']
        self.rat_opr_load_fact = raw_data['RAT_OPR_LOAD_FACT']
        self.rat_inv_load_cd = raw_data['RAT_INV_LOAD_CD']
        self.rat_inv_load_fact = raw_data['RAT_INV_LOAD_FACT']
        self.gen_opr_status = raw_data['GEN_OPR_STATUS']
        self.brg_posting = raw_data['BRG_POSTING']
        self.calc_str_eval = raw_data['CALC_STR_EVAL']
        self.calc_deck_geom = raw_data['CALC_DECK_GEOM']
        self.calc_undc = raw_data['CALC_UNDC']
        self.ww_adequacy_cd = raw_data['WW_ADEQUACY_CD']
        self.apprh_algn_cd = raw_data['APPRH_ALGN_CD']
        self.survey_railing = raw_data['SURVEY_RAILING']
        self.survey_transition = raw_data['SURVEY_TRANSITION']
        self.survey_guardrail = raw_data['SURVEY_GUARDRAIL']
        self.survey_rail_ends = raw_data['SURVEY_RAIL_ENDS']
        self.scour_crit_cd = raw_data['SCOUR_CRIT_CD']
        self.max_span_len = raw_data['MAX_SPAN_LEN']
        self.ovrl_str_len = raw_data['OVRL_STR_LEN']
        self.sidw_wd_l = raw_data['SIDW_WD_L']
        self.sidw_wd_r = raw_data['SIDW_WD_R']
        self.brg_rdw_wd = raw_data['BRG_RDW_WD']
        self.deck_wd = raw_data['DECK_WD']
        self.apprh_rdw_wd = raw_data['APPRH_RDW_WD']
        self.median_cd = raw_data['MEDIAN_CD']
        self.skew_deg = raw_data['SKEW_DEG']
        self.flared_sw = raw_data['FLARED_SW']
        self.min_horiz_clr_c = raw_data['MIN_HORIZ_CLR_C']
        self.minvrt_undclr_c = raw_data['MINVRT_UNDCLR_C']
        self.impr_typ_work_cd = raw_data['IMPR_TYP_WORK_CD']
        self.impr_typ_means_cd = raw_data['IMPR_TYP_MEANS_CD']
        self.impr_lng = raw_data['IMPR_LNG']
        self.impr_brg_cost = raw_data['IMPR_BRG_COST']
        self.impr_rdw_cost = raw_data['IMPR_RDW_COST']
        self.impr_tot_proj_cost = raw_data['IMPR_TOT_PROJ_COST']
        self.impr_cost_est_yr = raw_data['IMPR_COST_EST_YR']
        self.future_adt = raw_data['FUTURE_ADT']
        self.future_adt_yr = raw_data['FUTURE_ADT_YR']
        self.dedicated_nme = raw_data['DEDICATED_NME']
        self.invent_pref_rte = raw_data['INVENT_PREF_RTE']
        self.major_brg_sw = raw_data['MAJOR_BRG_SW']
        self.invent_county = raw_data['INVENT_COUNTY']
        self.seismic_suscept_cd = raw_data['SEISMIC_SUSCEPT_CD']
        self.gasb_34_sw = raw_data['GASB_34_SW']
        self.aperture_fabr_sw = raw_data['APERTURE_FABR_SW']
        self.aperture_orig_sw = raw_data['APERTURE_ORIG_SW']
        self.aperture_rep_sw = raw_data['APERTURE_REP_SW']
        self.orig_proj_nbr = raw_data['ORIG_PROJ_NBR']
        self.std_drw_nbr = raw_data['STD_DRW_NBR']
        self.microfilm_nbr = raw_data['MICROFILM_NBR']
        self.remarks = raw_data['REMARKS']
        self.utl_electric_sw = raw_data['UTL_ELECTRIC_SW']
        self.utl_gas_sw = raw_data['UTL_GAS_SW']
        self.utl_sewer_sw = raw_data['UTL_SEWER_SW']
        self.nbis_bridge_length = raw_data['NBIS_BRIDGE_LENGTH']
        self.rte_und_brg_cd = raw_data['RTE_UND_BRG_CD']
        self.load_rat_pct = raw_data['LOAD_RAT_PCT']
        self.load_rat_yr = raw_data['LOAD_RAT_YR']
        self.rating_soft_cd = raw_data['RATING_SOFT_CD']
        self.catwalks_sw = raw_data['CATWALKS_SW']
        self.retire_reason_cd = raw_data['RETIRE_REASON_CD']
        self.rec_add_dt = raw_data['REC_ADD_DT']
        self.mpo_cd = raw_data['MPO_CD']
        self.temp_subdecking_sw = raw_data['TEMP_SUBDECKING_SW']
        self.apprh_slab_sw = raw_data['APPRH_SLAB_SW']
        self.median_typ1_cd = raw_data['MEDIAN_TYP1_CD']
        self.median_typ2_cd = raw_data['MEDIAN_TYP2_CD']
        self.median_typ3_cd = raw_data['MEDIAN_TYP3_CD']
        self.railing_typ_cd = raw_data['RAILING_TYP_CD']
        self.composite_str_cd = raw_data['COMPOSITE_STR_CD']
        self.elas_strp_trou2_sw = raw_data['ELAS_STRP_TROU2_SW']
        self.elas_strp_trou3_sw = raw_data['ELAS_STRP_TROU3_SW']
        self.fencing_sw = raw_data['FENCING_SW']
        self.glare_screen_sw = raw_data['GLARE_SCREEN_SW']
        self.noise_barrier_sw = raw_data['NOISE_BARRIER_SW']
        self.deck_area = raw_data['DECK_AREA']
        self.curb_sidw_mtl_l = raw_data['CURB_SIDW_MTL_L']
        self.curb_sidw_mtl_r = raw_data['CURB_SIDW_MTL_R']
        self.curb_sidw_typ_l = raw_data['CURB_SIDW_TYP_L']
        self.curb_sidw_typ_r = raw_data['CURB_SIDW_TYP_R']
        self.hinge_cd = raw_data['HINGE_CD']
        self.deck_drn_cd = raw_data['DECK_DRN_CD']
        self.deck_conc_typ_cd = raw_data['DECK_CONC_TYP_CD']
        self.expn_joint1_cd = raw_data['EXPN_JOINT1_CD']
        self.expn_joint2_cd = raw_data['EXPN_JOINT2_CD']
        self.expn_joint3_cd = raw_data['EXPN_JOINT3_CD']
        self.horiz_crv_radius = raw_data['HORIZ_CRV_RADIUS']
        self.bearing_device1_cd = raw_data['BEARING_DEVICE1_CD']
        self.bearing_device2_cd = raw_data['BEARING_DEVICE2_CD']
        self.framing_typ_cd = raw_data['FRAMING_TYP_CD']
        self.haunch_gird_sw = raw_data['HAUNCH_GIRD_SW']
        self.long_memb_typ_cd = raw_data['LONG_MEMB_TYP_CD']
        self.main_mem_cd = raw_data['MAIN_MEM_CD']
        self.str_steel_prot_cd = raw_data['STR_STEEL_PROT_CD']
        self.pred_str_steel_typ = raw_data['PRED_STR_STEEL_TYP']
        self.paint_surface_area = raw_data['PAINT_SURFACE_AREA']
        self.str_steel_paint_cd = raw_data['STR_STEEL_PAINT_CD']
        self.post_tension_sw = raw_data['POST_TENSION_SW']
        self.abut_fwd_typ_cd = raw_data['ABUT_FWD_TYP_CD']
        self.abut_fwd_matl_cd = raw_data['ABUT_FWD_MATL_CD']
        self.abut_fwd_cd = raw_data['ABUT_FWD_CD']
        self.abut_rear_typ_cd = raw_data['ABUT_REAR_TYP_CD']
        self.abut_rear_matl_cd = raw_data['ABUT_REAR_MATL_CD']
        self.abut_rear_cd = raw_data['ABUT_REAR_CD']
        self.pred_pier_typ_cd = raw_data['PRED_PIER_TYP_CD']
        self.pred_pier_matl_cd = raw_data['PRED_PIER_MATL_CD']
        self.pier_pred_cd = raw_data['PIER_PRED_CD']
        self.pier_1_typ_cd = raw_data['PIER_1_TYP_CD']
        self.pier_1_matl_cd = raw_data['PIER_1_MATL_CD']
        self.pier_oth1_cd = raw_data['PIER_OTH1_CD']
        self.slope_prot_typ_cd = raw_data['SLOPE_PROT_TYP_CD']
        self.culvert_typ_cd = raw_data['CULVERT_TYP_CD']
        self.culvert_len = raw_data['CULVERT_LEN']
        self.culvert_fill_depth = raw_data['CULVERT_FILL_DEPTH']
        self.scenic_waterway_sw = raw_data['SCENIC_WATERWAY_SW']
        self.chan_prot_type_cd = raw_data['CHAN_PROT_TYPE_CD']
        self.stream_velocity = raw_data['STREAM_VELOCITY']
        self.hist_typ_cd = raw_data['HIST_TYP_CD']
        self.hist_builder_cd = raw_data['HIST_BUILDER_CD']
        self.suff_rating = raw_data['SUFF_RATING']
        self.defic_func_rating = raw_data['DEFIC_FUNC_RATING']
        self.main_str_descr_cd = raw_data['MAIN_STR_DESCR_CD']
        self.apprh_str_descr_cd = raw_data['APPRH_STR_DESCR_CD']
        self.hist_build_yr = raw_data['HIST_BUILD_YR']
        self.nlfid = raw_data['NLFID']
        self.ctl_begin_nbr = raw_data['CTL_BEGIN_NBR']
        self.route_type = raw_data['ROUTE_TYPE']
        self.route_nbr = raw_data['ROUTE_NBR']
        self.route_suffix = raw_data['ROUTE_SUFFIX']
        self.routine_insp_due = raw_data['ROUTINE_INSP_DUE']
        self.frac_crit_insp_due = raw_data['FRAC_CRIT_INSP_DUE']
        self.dive_insp_due = raw_data['DIVE_INSP_DUE']
        self.spcl_insp_due = raw_data['SPCL_INSP_DUE']
        self.bia_report = raw_data['BIA_REPORT']
        self.state_route_br_photos = raw_data['STATE_ROUTE_BR_PHOTOS']
        self.jurisdiction = raw_data['JURISDICTION']
        self.divided_hwy = raw_data['DIVIDED_HWY']
        self.access_control = raw_data['ACCESS_CONTROL']
        self.urban_area_code = raw_data['URBAN_AREA_CODE']
        self.base_type = raw_data['BASE_TYPE']
        self.functional_class = raw_data['FUNCTIONAL_CLASS']
        self.hpms_sample_id = raw_data['HPMS_SAMPLE_ID']
        self.lanes = raw_data['LANES']
        self.maintenance_authority = raw_data['MAINTENANCE_AUTHORITY']
        self.nhs = raw_data['NHS']
        self.priority_system = raw_data['PRIORITY_SYSTEM']
        self.surface_type = raw_data['SURFACE_TYPE']
        self.surface_width = raw_data['SURFACE_WIDTH']
        self.esal_total = raw_data['ESAL_TOTAL']
        self.pave_type = raw_data['PAVE_TYPE']
        self.pcr_year = raw_data['PCR_YEAR']
        self.roadway_width_nbr = raw_data['ROADWAY_WIDTH_NBR']
        self.created_user = raw_data['created_user']
        self.created_date = raw_data['created_date']
        self.last_edited_user = raw_data['last_edited_user']
        self.last_edited_date = raw_data['last_edited_date']

        self.photo_url = ''
        self.plan_sets_list = []

        self.latitude = self.latitude_dd
        self.longitude = self.longitude_dd

        self.map = self.get_map()

    def get_map(self):
        """
        Mapping function using folium JS package,

        :return:
            Folium javascript map object
        """
        f = folium.Figure(width=1500, height=700)

        m = folium.Map(
            width=1500,
            height=700,
            location=[self.latitude, self.longitude],
            zoom_start=14
        ).add_to(f)

        folium.Marker(
            location=[self.latitude, self.longitude],
            popup=f"{self.sfn}<br><br>Lat: {self.latitude}<br>Long: {self.longitude}",
            tooltip=self.sfn,
            icon=folium.Icon(icon="info-sign"),
        ).add_to(m)

        return m


def get_3_digit_st_cd_from_2(code):
    for key, value in NBIS_state_codes.items():
        if key[:-1] == str(code):
            code = key

    return code


def convert_longitudinal_values(longitude):
    """
    Takes a Longitude in degree minutes seconds, converts it to decimal, prints an error if it's not in North
    America

    return: converted value
    """

    longitude_deg = int(str(longitude)[:2])
    longitude_min = int(str(longitude)[2:4]) / 60
    longitude_sec = (int(str(round(longitude))[4:]) / 100) / 3600

    if longitude_deg + longitude_min + longitude_sec > 0:
        print('\nLongitude Values are supposed to be negative, performing conversion, '
              'but database potentially needs corrected\n')
        converted_value = -1 * (longitude_deg + longitude_min + longitude_sec)
    else:
        converted_value = longitude_deg + longitude_min + longitude_sec

    if converted_value > 0 or converted_value < -180:
        print("\nLongitude outside the range of continental US, check values, should be negative\n")

    return f"{converted_value:.6f}"


def get_df_from_url(url):
    r = requests.get(url)
    if r.ok:
        df = pd.read_csv(io.BytesIO(r.content), low_memory=False, quotechar="'")
    else:
        print(f"Couldn't find a dataframe at {url} make sure this page is still up")
        df = None

    return df


def convert_latitudinal_values(latitude):
    """
    Takes a Longitude in degree minutes seconds, converts it to decimal, prints an error if it's not in North
    America

    return: converted value
    """
    latitude_deg = int(str(latitude)[:2])
    latitude_min = int(str(latitude)[2:4]) / 60
    latitude_sec = (int(str(round(latitude))[4:]) / 100) / 3600

    converted_value = latitude_deg + latitude_min + latitude_sec

    if latitude_deg > 55 or latitude_deg < 16:
        print("Latitude outside the range of continental US, check values")

    return f"{converted_value:.6f}"


def convert_place_code(code):
    """
    NOTE: There is no coversion here, the SNBI update still uses FIPS Place codes, but those aren't readable
    so here's how to convert them, it also checks for bad values.

    Takes in bridge SFN, returns FIPS County Code location conversion,

    //TODO - Download FIPS definitions for various states, currently configured for only Ohio

    returns: Human readable version of 5 digit fips code
    """
    # Searches ohio fips results and converts the township and county to readable values
    results_df = ohio_fips[ohio_fips['FIPS CODE'] == int(code)][['COUNTY CODE', 'TOWNSHIP']]
    cty_cd = [i for i in ohio_counties if ohio_counties[i] == results_df.values[0][0]][0]
    twn_nme = results_df.values[0][1]

    readable_name = f"County: {cty_cd}   Township: {twn_nme}"

    if ohio_fips[ohio_fips['FIPS CODE'] == int(code)].empty:
        print("\nError, Place value not found in conversion data, double check the value")
        print("Is a legitimate entry in the FIPS 'place code' system\n")
    else:
        return readable_name


def state_code_conversion(code):
    """
    Takes in a bridge number, returns converted state code from index lookup

    returns converted value, since this is written for Ohio, 39
    """
    if len(str(code)) == 2:
        state_code = NBIS_state_codes[get_3_digit_st_cd_from_2(code)]
    else:
        state_code = NBIS_state_codes[code]

    return state_code


def get_cty_from_code(cty_code, st_code):
    """

    //TODO - Use geocoding spatial joints with GPS coords to verify bentley value against
    result from geocoding library (verify county codes)

    //TODO - Make function not specific to Ohio by replacing "OH" below with appropriate dict

    returns: 3 character numeric county code
    """
    # Uses a list comprehesion to go through counties and match full name with county code in database
    county_cd = f'{int(cty_code)}'.rjust(3, '0')
    lookup_cd = str(st_code) + county_cd

    county_name = fips_codes[fips_codes['fips'] == int(lookup_cd)]['name'].values[0]

    return county_name


factors_for_design_feature = {
    "Lane_Width_Rural": ["Function Classification", "Traffic Data", "Terrain", "Design Speed"],
    "Lane_Width_Urban": ["Function Classification", "Local"],
    "Shoulder_Width_Type_Rural": ["Function Classification", "Traffic Data"],
    "Shoulder_Width_Type_Urban": ["Function Classification", "Local"],
    "Guardrail_Offset": ["Function Classification", "Traffic Data"],
    "Degree_of_Curvature ": ["Local", "Design Speed"],
    "Grades": ["Function Classification", "Terrain", "Local", "Design Speed"],
    "Bridge_Clearances": ["Function Classification", "Traffic Data"],
    "Stopping_Sight_Distance": ["Design Speed"],
    "Passing_Intersection_Sight_Distances": ["Design Speed"],
    "Decision_Sight_Distance": ["Design Speed"],
    "Superelevation": ["Local", "Design Speed"],
    "Curve_Widening": ["Design Speed"],
    "Design_Speed_Rural": ["Function Classification", "Traffic Data", "Terrain"],
    "Design_Speed_Urban": ["Function Classification", "Local"],
    "Vertical_Alignment": ["Function Classification", "Terrain", "Local", "Design Speed"],
    "Horizontal_Alignment": ["Local", "Design Speed"]
}

design_feature_criteria = {
    "Lane_Width": {"Sections": ["301.1.2", "303.1"], "Figures": ["301-2", "301-4", "303-1"]},
    "Shoulder_Width": {"Sections": ["301.2.3", "303.1"], "Figures": ["301-3", "301-4", "303-1"]},
    "Design_Loading_Structural_Capacity": {"Sections": ["302.1"], "Figures": ["BDM"]},
    "Horizontal_Curve_Radius": {"Sections": ["202.3"], "Figures": ["202-2"]},
    "Maximum_Grade": {"Sections": ["203.2"], "Figures": ["203-1"]},
    "Stopping_Sight_Distance": {"Sections": ["201.2"], "Figures": ["201-1", "203-3", "203-4"]},
    "Pavement_Cross_Slope": {"Sections": ["301.1.5"], "Figures": [""]},
    "Superelevation": {"Sections": ["202.4.1", "202.4.3"], "Figures": ["202-3", "202-7", "202-8", "202-9", "202-10"]},
    "Vertical_Clearance": {"Sections": ["302.1"], "Figures": ["302-1", "302-2", "302-3"]},
}


fips_url = "https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_and_county_fips_master.csv"
fips_codes = get_df_from_url(fips_url)

ohio_fips = get_df_from_url("https://daneparks.com/Dane/civilpy/-/raw/master/res/2022AllRecordsDelimitedAllStates.txt")


def get_historic_bridge_data(sfn=2701464, state='Ohio'):
    """
    Gets historic bridge values for a given sfn

    // TODO - Create database of values to speed this up
    """
    if state == 'Ohio':
        nbi_df = get_df_from_url(
            "https://daneparks.com/Dane/civilpy/-/raw/snibi_tests_development/res/Ohio_NBI.txt")
    else:
        nbi_df = get_df_from_url(
            "https://daneparks.com/Dane/civilpy/-/raw/snibi_tests_development/res/2022AllRecordsDelimitedAllStates.txt"
        )

    first_bridge_data = nbi_df[nbi_df['STRUCTURE_NUMBER_008'].str.strip() == sfn]

    return first_bridge_data


def get_project_data_from_tims(pid: str = '96213'):
    """
    Uses the TIMS REST API to return json values for a given bridge sfn.

    :parameter
        pid (str): Project ID number used to look up project points (PID)

    :returns:
        dict containing the project points and the number of points
    """

    url_1 = f"https://gis.dot.state.oh.us/arcgis/rest/services/TIMS/Projects/MapServer/0/query?where=PID_NBR%3D{pid}&te"
    url_2 = "xt=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects"
    url_3 = "&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecisio"
    url_4 = "n=&outSR=&having=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outS"
    url_5 = "tatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset"
    url_6 = "&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeVal"
    url_7 = "ues=&quantizationParameters=&featureEncoding=esriDefault&f=html"

    url = url_1 + url_2 + url_3 + url_3 + url_4 + url_5 + url_6 + url_7

    s = requests.Session()
    page = s.get(url)
    url_base = 'https://gis.dot.state.oh.us'
    soup = BeautifulSoup(page.content, 'html5lib')
    s.close()

    all_page_links = soup.find_all('a')
    project_point_links = {}
    counter = 0

    for link in all_page_links:
        if link.text.isnumeric():
            counter += 1
            full_data_url = url_base + link.get('href') + '?f=pjson'
            print(f"\nRetrieving data from url at {full_data_url}")

            page = s.get(full_data_url)
            # Added ordered dict value to attempt to return values in same order
            # noinspection PyTypeChecker
            data_json = page.json(object_pairs_hook=OrderedDict)
            s.close()

            try:
                extracted_data = data_json['feature']['attributes']
            except KeyError:
                return data_json

            project_point_links[link.text] = extracted_data

        else:
            pass

    project_point_links['no_of_pts'] = counter

    return project_point_links


class Project:
    def __init__(self, pid: str = '96213'):
        self.PID = pid
        raw_data = get_project_data_from_tims(pid)
        # Uses the first point returned from the query to set the general class attributes
        single_dict = raw_data[list(raw_data.keys())[0]]

        self.objectid = single_dict['ObjectID']
        self.gis_id = single_dict['GIS_ID']
        self.pid_nbr = single_dict['PID_NBR']
        self.district_nbr = single_dict['DISTRICT_NBR']
        self.locale_short_nme = single_dict['LOCALE_SHORT_NME']
        self.county_nme = single_dict['COUNTY_NME']
        self.project_nme = single_dict['PROJECT_NME']
        self.contract_type = single_dict['CONTRACT_TYPE']
        self.primary_fund_category_txt = single_dict['PRIMARY_FUND_CATEGORY_TXT']
        self.project_manager_nme = single_dict['PROJECT_MANAGER_NME']
        self.reservoir_year = single_dict['RESERVOIR_YEAR']
        self.tier = single_dict['TIER']
        self.odot_letting = single_dict['ODOT_LETTING']
        self.schedule_type_short_nme = single_dict['SCHEDULE_TYPE_SHORT_NME']
        self.env_project_manager_nme = single_dict['ENV_PROJECT_MANAGER_NME']
        self.area_engineer_nme = single_dict['AREA_ENGINEER_NME']
        self.project_engineer_nme = single_dict['PROJECT_ENGINEER_NME']
        self.design_agency = single_dict['DESIGN_AGENCY']
        self.sponsoring_agency = single_dict['SPONSORING_AGENCY']
        self.pdp_short_name = single_dict['PDP_SHORT_NAME']
        self.primary_work_category = single_dict['PRIMARY_WORK_CATEGORY']
        self.project_status = single_dict['PROJECT_STATUS']
        self.fiscal_year = single_dict['FISCAL_YEAR']
        self.inhouse_design_full_nme = single_dict['INHOUSE_DESIGN_FULL_NME']
        self.est_total_constr_cost = single_dict['EST_TOTAL_CONSTR_COST']
        self.state_project_nbr = single_dict['STATE_PROJECT_NBR']
        self.constr_vendor_nme = single_dict['CONSTR_VENDOR_NME']
        self.stip_flag = single_dict['STIP_FLAG']
        self.current_stip_co_amt = single_dict['CURRENT_STIP_CO_AMT']
        self.project_plans_url = single_dict['PROJECT_PLANS_URL']
        self.project_addenda_url = single_dict['PROJECT_ADDENDA_URL']
        self.project_proposal_url = single_dict['PROJECT_PROPOSAL_URL']
        self.fmis_proj_desc = single_dict['FMIS_PROJ_DESC']
        self.award_milestone_dt = single_dict['AWARD_MILESTONE_DT']
        self.begin_constr_milestone_dt = single_dict['BEGIN_CONSTR_MILESTONE_DT']
        self.end_constr_milestone_dt = single_dict['END_CONSTR_MILESTONE_DT']
        self.open_traffic_dt = single_dict['OPEN_TRAFFIC_DT']
        self.central_office_close_dt = single_dict['CENTRAL_OFFICE_CLOSE_DT']
        self.source_last_updated = single_dict['SOURCE_LAST_UPDATED']
        self.cod_last_updated = single_dict['COD_LAST_UPDATED']
        self.preserv_funds_ind = single_dict['PRESERV_FUNDS_IND']
        self.major_brg_funds_ind = single_dict['MAJOR_BRG_FUNDS_IND']
        self.major_new_funds_ind = single_dict['MAJOR_NEW_FUNDS_IND']
        self.major_rehab_funds_ind = single_dict['MAJOR_REHAB_FUNDS_IND']
        self.mpo_funds_ind = single_dict['MPO_FUNDS_IND']
        self.safety_funds_ind = single_dict['SAFETY_FUNDS_IND']
        self.local_funds_ind = single_dict['LOCAL_FUNDS_IND']
        self.other_funds_ind = single_dict['OTHER_FUNDS_IND']
        self.nlf_id = single_dict['NLF_ID']
        self.ctl_begin = single_dict['CTL_BEGIN']
        self.ctl_end = single_dict['CTL_END']
        self.gis_feature_type = single_dict['GIS_FEATURE_TYPE']
        self.route_type = single_dict['ROUTE_TYPE']
        self.route_id = single_dict['ROUTE_ID']
        self.structure_file_nbr = single_dict['STRUCTURE_FILE_NBR']
        self.main_structure_type = single_dict['MAIN_STRUCTURE_TYPE']
        self.sufficiency_rating = single_dict['SUFFICIENCY_RATING']
        self.ovrl_structure_length = single_dict['OVRL_STRUCTURE_LENGTH']
        self.deck_area = single_dict['DECK_AREA']
        self.deck_width = single_dict['DECK_WIDTH']
        self.feature_intersect = single_dict['FEATURE_INTERSECT']
        self.year_built = single_dict['YEAR_BUILT']
        self.longitude_begin_nbr = single_dict['LONGITUDE_BEGIN_NBR']
        self.latitude_begin_nbr = single_dict['LATITUDE_BEGIN_NBR']
        self.longitude_end_nbr = single_dict['LONGITUDE_END_NBR']
        self.latitude_end_nbr = single_dict['LATITUDE_END_NBR']
        self.county_cd_work_location = single_dict['COUNTY_CD_WORK_LOCATION']
        self.county_nme_work_location = single_dict['COUNTY_NME_WORK_LOCATION']
        self.district_work_location = single_dict['DISTRICT_WORK_LOCATION']
        self.pavement_treatment_type = single_dict['PAVEMENT_TREATMENT_TYPE']
        self.pavement_treatment_category = single_dict['PAVEMENT_TREATMENT_CATEGORY']
        self.created_user = single_dict['created_user']
        self.created_date = single_dict['created_date']
        self.last_edited_user = single_dict['last_edited_user']
        self.last_edited_date = single_dict['last_edited_date']
