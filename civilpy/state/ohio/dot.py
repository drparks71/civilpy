import os
import re
import folium
import pandas as pd
from pathlib import Path
# from PIL import Image, ImageSequence
import math
import tifftools
from natsort import natsorted
from bs4 import BeautifulSoup
import json
import requests
import pint
import time
from datetime import datetime

units = pint.UnitRegistry()


def help_function():
    """
    To use the dicts, import them into python, and then use the two letter code to get the translations, i.e.
    basemap_labels['BA'] will return "Aerial Mapping"

    General Notes:
    General File Naming Format:
        nnnnn(n)_aa###.dgn where:
            nnnnnn - 5 (or 6) digit PID
            aa     - Two letter code signifying sheet type (see dicts)
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

fips_codes = pd.read_csv("https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_and_county_fips_master.csv")
ohio_fips = pd.read_csv("https://daneparks.com/Dane/civilpy/-/raw/master/res/ohio_fips.csv")

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


def get_bridge_data_from_tims(sfn=6500609):
    """
    Function to return Bridge data from ODOT TIMS REST server

    # //TODO - Integrate with ESRIs python package or rewrite function in a way that gives users more search tools

    :param sfn: Bridge structure file number
    :return: A dictionary containing all the values relevant to the desired bridge
    """
    url = f"https://gis.dot.state.oh.us/arcgis/rest/services/TIMS/Assets/MapServer/5/query?where=sfn%3D{sfn}&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=html"
    page = requests.get(url, timeout=5)
    soup = BeautifulSoup(page.content, 'html5lib')

    bridge_link = soup.find_all('a')

    full_data_url = "https://gis.dot.state.oh.us/" + bridge_link[-1].get('href')
    full_data_url_json = full_data_url + '?f=pjson'

    print(f"\nRetrieving data from url at {full_data_url_json}\n")

    page = requests.get(full_data_url_json)
    data_json = json.loads(page.content)

    extracted_data = data_json['feature']['attributes']

    return extracted_data


class BridgeObject:
    """
    General Bridge object to hold data from ODOT TIMS REST SERVER
    """

    def __init__(self, sfn):
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
        Mapping function using folium JS package, //TODO - Determine a way to test this function
        :return:
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


class SNBITransition(BridgeObject):
    """
    Class to hold bridge data and compare it to historic reported values, for the standard object to get
    bridge data from tims, see the 'BridgeObject' class

    # //TODO - Build fake bridge w/ bad data to ensure failing cases work
    """

    def __init__(self, sfn, leading_zeros=0):
        """
        Additional inputs to BridgeObject Class:

        leading_zeros - Configuration value for SNIBI Transfer
        leading zeros, accepts values from 0-2 under the following
        coding;
            0 - Do not Pad (default)
            1 - Pad number w/ single zero?
            2 - Pad w/ 0s to 15
        """

        super().__init__(sfn)
        self.historic_data = {}
        print(
            'Getting historic NBIS Data, this step is slow...')  # //TODO - This is slow w/ all bridges, could be sped up by filtering
        self.historic_data = get_historic_bridge_data(sfn)

        if leading_zeros == 0:
            self.bridge_number = f"{self.sfn}"
        elif leading_zeros == 1:
            self.bridge_number = f"{str(self.sfn).zfill(len(str(self.sfn)))}"
        elif leading_zeros == 2:
            self.bridge_number = f"{str(self.sfn).zfill(15)}"

        # This is a list of every check, or test that is run against the values
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
            'BN01': '',
            'BN02': '',
            'BN03': '',
            'BN04': '',
            'BN05': '',
            'BN06': '',
            'BLR01': '',
            'BLR02': '',
            'BLR03': '',
            'BLR04': '',
            'BLR05': '',
            'BLR06': '',
            'BLR07': '',
            'BLR08': '',
            'BPS01': '',
            'BPS02': '',
            'BEP01': '',
            'BEP02': '',
            'BEP03': '',
            'BEP04': '',
            'BIR01': '',
            'BIR02': '',
            'BIR03': '',
            'BIR04': '',
            'BIE01': '',
            'BIE02': '',
            'BIE03': '',
            'BIE04': '',
            'BIE05': '',
            'BIE06': '',
            'BIE07': '',
            'BIE08': '',
            'BIE09': '',
            'BIE10': '',
            'BIE11': '',
            'BIE12': '',
            'BC01': '',
            'BC02': '',
            'BC03': '',
            'BC04': '',
            'BC05': '',
            'BC06': '',
            'BC07': '',
            'BC08': '',
            'BC09': '',
            'BC10': '',
            'BC11': '',
            'BC12': '',
            'BC13': '',
            'BC14': '',
            'BC15': '',
            'BAP01': '',
            'BAP02': '',
            'BAP03': '',
            'BAP04': '',
            'BAP05': '',
            'BW01': '',
            'BW02': '',
            'BW03': '',
        }

    def bid01(self):
        """
        B.ID.01 Function - Bridge Number Comparison
        """
        historic = self.historic_data["STRUCTURE_NUMBER_008"].iloc[0].strip()
        modern = str(self.sfn)

        if historic == modern:
            return_var = None
        else:
            print(f"'B.ID_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto match")
            return_var = 'B.ID_01_CHECK_FAILED'

        return return_var

    def bid02(self):
        """
        B.L.12 Function - Metropolitan Planning Organization

        Previously didn't exist - Created as placeholder
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.ID_02_CHECK_FAILED'\n\nNot sure how, its a placeholder:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\nConversion: ")
            return_var = 'B.ID_02_CHECK_FAILED'

        return return_var

    def bid03(self):
        """
        B.ID.03 Function - Previous Bridge Number

        Previously didn't exist - Created as placeholder
        """
        historic = ''
        modern = ''

        if historic == modern:
            return_var = None
        else:
            print(f"'B.ID_03_CHECK_FAILED'\n\nNot sure how, its a placeholder:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto be equal\n\n\nConversion: ")
            return_var = 'BID_03_CHECK_FAILED'

        return return_var

    def bl01(self, state='Ohio'):
        """
        B.L.01 Function - State Code Comparison
        """
        historic = state_code_conversion(get_3_digit_st_cd_from_2(self.historic_data["STATE_CODE_001"].iloc[0]))
        modern = state

        if historic == modern:
            return_var = None
        else:
            print(f"'BL_01_CHECK_FAILED'\n\nExpected the values:\nHistoric: {historic}\n"
                  f"Modern: {modern}\n\nto match")
            return_var = 'BL_01_CHECK_FAILED'

        return return_var

    def bl02(self):
        """
        B.L.02 Function - County Code Comparison
        """
        county_name = get_cty_from_code(
            self.historic_data["COUNTY_CODE_003"].iloc[0],
            self.historic_data["STATE_CODE_001"].iloc[0])
        county_short = county_name.split(' ')[0]
        historic = ohio_counties[county_short.upper()]

        modern = self.county_cd

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

        # Gets the error from the new and old latitude in feet (estimate based on equator) returns an error if over
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
                      f"Modern: {modern}\n\nto be equal\n\n\nCode Conversion: {state_code_conversion(modern)}")
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
            return_var = 'B.LR_03_CHECK_FAILED'

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
            return_var = 'B.EP_04_CHECK_FAILED'

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

    def bc02(self):
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

    def bc03(self):
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

    def bc04(self):
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

    def bc05(self):
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

    def bc06(self):
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

    def bc07(self):
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

    def bc08(self):
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

    def bc09(self):
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

    def bc10(self):
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

    def bc11(self):
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

    def bc12(self):
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

    def bc13(self):
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

    def bc14(self):
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

    def bc15(self):
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

    def bap01(self):
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

    def bap02(self):
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

    def bap03(self):
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

    def bap04(self):
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

    def bap05(self):
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

    def bw01(self):
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

    def bw02(self):
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


def get_historic_bridge_data(sfn='2701464', state_code=39):
    """
    Gets historic bridge values for a given sfn

    // TODO - Create database of values to speed this up
    """
    nbi_df = pd.read_csv(
        "https://daneparks.com/Dane/civilpy/-/raw/snibi_tests_development/res/2022AllRecordsDelimitedAllStates.txt",
        low_memory=False, quotechar="'")
    # state_bridges = nbi_df[nbi_df['STATE_CODE_001'] == state_code]
    first_bridge_data = nbi_df[nbi_df['STRUCTURE_NUMBER_008'].str.strip() == sfn.strip()]

    return first_bridge_data


def get_project_data_from_tims(pid='112664'):
    url = f"https://gis.dot.state.oh.us/arcgis/rest/services/TIMS/Projects/MapServer/0/query?where=PID_NBR%3D{pid}&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=true&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=html"

    page = requests.get(url)
    url_base = 'https://gis.dot.state.oh.us'
    soup = BeautifulSoup(page.content, 'html5lib')

    all_page_links = soup.find_all('a')
    project_point_links = {}
    counter = 0

    for link in all_page_links:
        if link.text.isnumeric():
            counter += 1
            full_data_url = url_base + link.get('href') + '?f=pjson'
            print(f"\nRetrieving data from url at {full_data_url}")

            page = requests.get(full_data_url)
            data_json = json.loads(page.content)

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
    def __init__(self, pid):
        self.PID = pid
        raw_data = get_project_data_from_tims()
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

