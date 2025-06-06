"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Removed to stop hitting TIMs API
# import unittest
# from src.civilpy.state.ohio.dot import TimsBridge
# from civilpy.state.ohio.dot import Project
#
# # Import dicts to make sure they still exist
# from src.civilpy.state.ohio.dot import (
#     help_function,
#     basemap_labels,
#     bridge_labels,
#     drainage_labels,
# )
# from src.civilpy.state.ohio.dot import (
#     landscaping_labels,
#     lighting_labels,
#     mot_labels,
#     row_labels,
#     roadway_labels,
# )
# from src.civilpy.state.ohio.dot import (
#     signal_labels,
#     traffic_control_labels,
#     utility_labels,
#     wall_labels,
#     all_labels,
# )
# from src.civilpy.state.ohio.dot import (
#     ohio_counties,
#     NBIS_state_codes,
#     state_code_conversion,
#     get_3_digit_st_cd_from_2,
# )
# from src.civilpy.state.ohio.dot import geotechnical_labels
#
# # Import functions to test them
# from src.civilpy.state.ohio.dot import get_bridge_data_from_tims
#
#
# class TestDotFunctions(unittest.TestCase):
#     def test_help_function(self):
#         self.assertEqual(help_function(), None)
#
#     def test_dicts(self):
#         self.assertEqual(basemap_labels["KB"], "3D Model KB")
#         self.assertEqual(bridge_labels["SB"], "Bearing")
#         self.assertEqual(drainage_labels["XD"], "Channel Cross Sections")
#         self.assertEqual(geotechnical_labels["YL"], "Geohazard Boring Logs")
#         self.assertEqual(landscaping_labels["PD"], "Details")
#         self.assertEqual(lighting_labels["LC"], "Circuit Diagrams")
#         self.assertEqual(mot_labels["XM"], "Cross Sections")
#         self.assertEqual(row_labels["RC"], "Centerline Plat")
#         self.assertEqual(roadway_labels["GC"], "Calculations/Computations")
#         self.assertEqual(signal_labels["CD"], "Details")
#         self.assertEqual(traffic_control_labels["TC"], "Calculations/Computations")
#         self.assertEqual(utility_labels["UC"], "Calculations/Computations")
#         self.assertEqual(wall_labels["WC"], "Calculations/Computations")
#         self.assertEqual(all_labels["basemap_labels"]["KB"], "3D Model KB")
#         self.assertEqual(ohio_counties["ADAMS"], "ADA")
#         self.assertEqual(NBIS_state_codes["014"], "Alabama")
#
#     def test_get_bridge_data_from_tims(self):
#         self.assertEqual(get_bridge_data_from_tims()["SFN"], "6500609")
#
#     def test_state_code_conversion(self):
#         self.assertEqual(state_code_conversion(39), "Ohio")
#
#     def test_get_3_digit_st_cd_from_2(self):
#         self.assertEqual(get_3_digit_st_cd_from_2(39), "395")
#
#
# class TestBridgeObject(unittest.TestCase):
#     def setUp(self, sfn=6500609):
#         # Creates a 'test bridge' and makes sure none of the attributes have changed
#         self.tb = TimsBridge(sfn)
#
#     def tearDown(self):
#         pass
#
#     def test_init(self, sfn=6500609):
#         # Tests that all the attributes in the TIMS database haven't changed, uses sfn 6500609 by default, but can
#         # be changed to any SFN, //TODO - Update to a retired SFN to avoid non-tims related changes altering results
#         self.assertIsInstance(self.tb.objectid, int)
#
#     def test_tims_attributes_changes(self):
#         # Creates a 'test bridge' and makes sure none of the attributes have changed
#         self.assertEqual(self.tb.sfn, "6500609")
#         self.assertEqual(self.tb.str_loc_carried, "US 23SB")
#         self.assertEqual(self.tb.rte_on_brg_cd, "10")
#         self.assertEqual(self.tb.district, "06")
#         self.assertEqual(self.tb.county_cd, "PIC")
#         self.assertEqual(self.tb.invent_spcl_dsgt, "L")
#         self.assertEqual(self.tb.fips_cd, "62484")
#         self.assertEqual(self.tb.invent_on_und_cd, "1")
#         self.assertEqual(self.tb.invent_hwy_sys_cd, "2")
#         self.assertEqual(self.tb.invent_hwy_dsgt_cd, "1")
#         self.assertEqual(self.tb.invent_dir_sfx_cd, "0")
#         self.assertEqual(self.tb.invent_feat, "SCIPPO CR")
#         self.assertEqual(self.tb.str_loc, "1.6 MI N OF SR361")
#         self.assertEqual(self.tb.latitude_dd, 39.531378)
#         self.assertEqual(self.tb.longitude_dd, -82.967494)
#         self.assertEqual(self.tb.brdr_brg_state, None)
#         self.assertEqual(self.tb.brdr_brg_pct_resp, None)
#         self.assertEqual(self.tb.brdr_brg_sfn, None)
#         self.assertEqual(self.tb.main_str_mtl_cd, "4")
#         self.assertEqual(self.tb.main_str_type_cd, "02")
#         self.assertEqual(self.tb.apprh_str_mtl_cd, "0")
#         self.assertEqual(self.tb.apprh_str_type_cd, "00")
#         self.assertEqual(self.tb.main_spans, 3)
#         self.assertEqual(self.tb.apprh_spans, 0)
#         self.assertEqual(self.tb.deck_cd, "1")
#         self.assertEqual(self.tb.deck_prot_extl_cd, "N")
#         self.assertEqual(self.tb.deck_prot_int_cd, "1")
#         self.assertEqual(self.tb.wear_surf_dt, 1290556800000)
#         self.assertEqual(self.tb.wearing_surf_cd, "1")
#         self.assertEqual(self.tb.wearing_surf_thck, 1)
#         self.assertEqual(self.tb.paint_dt, 1290556800000)
#         self.assertEqual(self.tb.yr_built, -426124800000)
#         self.assertEqual(self.tb.maj_recon_dt, 1290556800000)
#         self.assertEqual(self.tb.type_serv1_cd, "1")
#         self.assertEqual(self.tb.type_serv2_cd, "5")
#         self.assertEqual(self.tb.lanes_on, 2)
#         self.assertEqual(self.tb.lanes_und, 0)
#         self.assertEqual(self.tb.invent_rte_adt, 12006)
#         self.assertEqual(self.tb.bypass_len, "12")
#         self.assertEqual(self.tb.nbis_len_sw, "Y")
#         self.assertEqual(self.tb.invent_nhs_cd, "1")
#         self.assertEqual(self.tb.func_clas_cd, "02")
#         self.assertEqual(self.tb.dfns_hwy_dsgt_sw, "0")
#         self.assertEqual(self.tb.parallel_str_cd, "L")
#         self.assertEqual(self.tb.dir_traffic_cd, "1")
#         self.assertEqual(self.tb.temp_str_sw, "")
#         self.assertEqual(self.tb.dsgt_natl_netw_sw, "0")
#         self.assertEqual(self.tb.toll_cd, "3")
#         self.assertEqual(self.tb.routine_resp_cd, "01")
#         self.assertEqual(self.tb.routine_resp_cd_2, "  ")
#         self.assertEqual(self.tb.maint_resp_cd, "01")
#         self.assertEqual(self.tb.maint_resp_cd_2, "  ")
#         self.assertEqual(self.tb.insp_resp_cd, "01")
#         self.assertEqual(self.tb.insp_resp_cd_2, "  ")
#         self.assertEqual(self.tb.hist_sgn_cd, "5")
#         self.assertEqual(self.tb.nav_control_sw, "0")
#         self.assertEqual(self.tb.nav_vrt_clr, 0)
#         self.assertEqual(self.tb.nav_horiz_clr, 0)
#         self.assertEqual(self.tb.subs_fenders, "1")
#         self.assertEqual(self.tb.min_nav_vrt_clr, 0)
#         self.assertEqual(self.tb.insp_dt, 1676246400000)
#         self.assertEqual(self.tb.dsgt_insp_freq, 24)
#         self.assertEqual(self.tb.frac_crit_insp_sw, "N")
#         self.assertEqual(self.tb.fraccrit_insp_freq, 0)
#         self.assertEqual(self.tb.frac_crit_insp_dt, None)
#         self.assertEqual(self.tb.dive_insp_sw, "N")
#         self.assertEqual(self.tb.dive_insp_freq, 0)
#         self.assertEqual(self.tb.dive_insp_dt, None)
#         self.assertEqual(self.tb.spcl_insp_sw, "N")
#         self.assertEqual(self.tb.spcl_insp_freq, 0)
#         self.assertEqual(self.tb.spcl_insp_dt, None)
#         self.assertEqual(self.tb.snooper_insp_sw, "N")
#         self.assertEqual(self.tb.deck_summary, "8")
#         self.assertEqual(self.tb.deck_wear_surf, "8")
#         self.assertEqual(self.tb.deck_expn_joints, "")
#         self.assertEqual(self.tb.sups_summary, "9")
#         self.assertEqual(self.tb.paint, "9")
#         self.assertEqual(self.tb.subs_summary, "9")
#         self.assertEqual(self.tb.chan_summary, "8")
#         self.assertEqual(self.tb.subs_scour, "9")
#         self.assertEqual(self.tb.culvert_summary, "N")
#         self.assertEqual(self.tb.gen_appraisal, "9")
#         self.assertEqual(self.tb.design_load_cd, "9")
#         self.assertEqual(self.tb.rat_opr_load_fact, "1130")
#         self.assertEqual(self.tb.rat_inv_load_cd, "8")
#         self.assertEqual(self.tb.rat_inv_load_fact, "0870")
#         self.assertEqual(self.tb.gen_opr_status, "A")
#         self.assertEqual(self.tb.brg_posting, "5")
#         self.assertEqual(self.tb.calc_str_eval, "7")
#         self.assertEqual(self.tb.calc_deck_geom, "8")
#         self.assertEqual(self.tb.calc_undc, "N")
#         self.assertEqual(self.tb.ww_adequacy_cd, "6")
#         self.assertEqual(self.tb.apprh_algn_cd, "8")
#         self.assertEqual(self.tb.survey_railing, "1")
#         self.assertEqual(self.tb.survey_transition, "1")
#         self.assertEqual(self.tb.survey_guardrail, "1")
#         self.assertEqual(self.tb.survey_rail_ends, "1")
#         self.assertEqual(self.tb.scour_crit_cd, "8")
#         self.assertEqual(self.tb.max_span_len, 65)
#         self.assertEqual(self.tb.ovrl_str_len, 175.5)
#         self.assertEqual(self.tb.sidw_wd_l, 0)
#         self.assertEqual(self.tb.sidw_wd_r, 0)
#         self.assertEqual(self.tb.brg_rdw_wd, 42)
#         self.assertEqual(self.tb.deck_wd, 45)
#         self.assertEqual(self.tb.apprh_rdw_wd, 42)
#         self.assertEqual(self.tb.median_cd, "0")
#         self.assertEqual(self.tb.skew_deg, 40)
#         self.assertEqual(self.tb.flared_sw, "0")
#         self.assertEqual(self.tb.min_horiz_clr_c, 42)
#         self.assertEqual(self.tb.minvrt_undclr_c, 0)
#         self.assertEqual(self.tb.impr_typ_work_cd, "  ")
#         self.assertEqual(self.tb.impr_typ_means_cd, " ")
#         self.assertEqual(self.tb.impr_lng, 0)
#         self.assertEqual(self.tb.impr_brg_cost, 0)
#         self.assertEqual(self.tb.impr_rdw_cost, 0)
#         self.assertEqual(self.tb.impr_tot_proj_cost, 0)
#         self.assertEqual(self.tb.impr_cost_est_yr, 0)
#         self.assertEqual(self.tb.future_adt, 16664)
#         self.assertEqual(self.tb.future_adt_yr, 2038)
#         self.assertEqual(self.tb.dedicated_nme, "")
#         self.assertEqual(self.tb.invent_pref_rte, "N")
#         self.assertEqual(self.tb.major_brg_sw, "N")
#         self.assertEqual(self.tb.invent_county, "DIS")
#         self.assertEqual(self.tb.seismic_suscept_cd, "N")
#         self.assertEqual(self.tb.gasb_34_sw, "Y")
#         self.assertEqual(self.tb.aperture_fabr_sw, "2")
#         self.assertEqual(self.tb.aperture_orig_sw, "2")
#         self.assertEqual(self.tb.aperture_rep_sw, "1")
#         self.assertEqual(self.tb.orig_proj_nbr, "044955")
#         self.assertEqual(self.tb.std_drw_nbr, "")
#         self.assertEqual(self.tb.microfilm_nbr, "PIC003")
#         self.assertEqual(self.tb.remarks, "")
#         self.assertEqual(self.tb.utl_electric_sw, "N")
#         self.assertEqual(self.tb.utl_gas_sw, "N")
#         self.assertEqual(self.tb.utl_sewer_sw, "N")
#         self.assertEqual(self.tb.nbis_bridge_length, 175.5)
#         self.assertEqual(self.tb.rte_und_brg_cd, "99")
#         self.assertEqual(self.tb.load_rat_pct, 150)
#         self.assertEqual(self.tb.load_rat_yr, 2023)
#         self.assertEqual(self.tb.rating_soft_cd, "3")
#         self.assertEqual(self.tb.catwalks_sw, "N")
#         self.assertEqual(self.tb.retire_reason_cd, "")
#         self.assertEqual(self.tb.rec_add_dt, -2208988800000)
#         self.assertEqual(self.tb.mpo_cd, "NN")
#         self.assertEqual(self.tb.temp_subdecking_sw, "N")
#         self.assertEqual(self.tb.apprh_slab_sw, "Y")
#         self.assertEqual(self.tb.median_typ1_cd, "N")
#         self.assertEqual(self.tb.median_typ2_cd, "N")
#         self.assertEqual(self.tb.median_typ3_cd, "N")
#         self.assertEqual(self.tb.railing_typ_cd, "I")
#         self.assertEqual(self.tb.composite_str_cd, "Y")
#         self.assertEqual(self.tb.elas_strp_trou2_sw, "N")
#         self.assertEqual(self.tb.elas_strp_trou3_sw, "N")
#         self.assertEqual(self.tb.fencing_sw, "N")
#         self.assertEqual(self.tb.glare_screen_sw, "N")
#         self.assertEqual(self.tb.noise_barrier_sw, "N")
#         self.assertEqual(self.tb.deck_area, 7898)
#         self.assertEqual(self.tb.curb_sidw_mtl_l, "N")
#         self.assertEqual(self.tb.curb_sidw_mtl_r, "N")
#         self.assertEqual(self.tb.curb_sidw_typ_l, "N")
#         self.assertEqual(self.tb.curb_sidw_typ_r, "N")
#         self.assertEqual(self.tb.hinge_cd, "N")
#         self.assertEqual(self.tb.deck_drn_cd, "0")
#         self.assertEqual(self.tb.deck_conc_typ_cd, "B")
#         self.assertEqual(self.tb.expn_joint1_cd, "N")
#         self.assertEqual(self.tb.expn_joint2_cd, "N")
#         self.assertEqual(self.tb.expn_joint3_cd, "N")
#         self.assertEqual(self.tb.horiz_crv_radius, "")
#         self.assertEqual(self.tb.bearing_device1_cd, "C")
#         self.assertEqual(self.tb.bearing_device2_cd, "N")
#         self.assertEqual(self.tb.framing_typ_cd, "4")
#         self.assertEqual(self.tb.haunch_gird_sw, "N")
#         self.assertEqual(self.tb.long_memb_typ_cd, "N")
#         self.assertEqual(self.tb.main_mem_cd, "1")
#         self.assertEqual(self.tb.str_steel_prot_cd, "5")
#         self.assertEqual(self.tb.pred_str_steel_typ, "D")
#         self.assertEqual(self.tb.paint_surface_area, 25457)
#         self.assertEqual(self.tb.str_steel_paint_cd, "2")
#         self.assertEqual(self.tb.post_tension_sw, "N")
#         self.assertEqual(self.tb.abut_fwd_typ_cd, "D")
#         self.assertEqual(self.tb.abut_fwd_matl_cd, "2")
#         self.assertEqual(self.tb.abut_fwd_cd, "A")
#         self.assertEqual(self.tb.abut_rear_typ_cd, "D")
#         self.assertEqual(self.tb.abut_rear_matl_cd, "2")
#         self.assertEqual(self.tb.abut_rear_cd, "A")
#         self.assertEqual(self.tb.pred_pier_typ_cd, "1")
#         self.assertEqual(self.tb.pred_pier_matl_cd, "2")
#         self.assertEqual(self.tb.pier_pred_cd, "A")
#         self.assertEqual(self.tb.pier_1_typ_cd, "N")
#         self.assertEqual(self.tb.pier_1_matl_cd, "N")
#         self.assertEqual(self.tb.pier_oth1_cd, "N")
#         self.assertEqual(self.tb.slope_prot_typ_cd, "3")
#         self.assertEqual(self.tb.culvert_typ_cd, "N")
#         self.assertEqual(self.tb.culvert_len, 0)
#         self.assertEqual(self.tb.culvert_fill_depth, 0)
#         self.assertEqual(self.tb.scenic_waterway_sw, "N")
#         self.assertEqual(self.tb.chan_prot_type_cd, "5")
#         self.assertEqual(self.tb.stream_velocity, "00000")
#         self.assertEqual(self.tb.hist_typ_cd, "330")
#         self.assertEqual(self.tb.hist_builder_cd, "192")
#         self.assertEqual(self.tb.suff_rating, "086.1")
#         self.assertEqual(self.tb.defic_func_rating, "0")
#         self.assertEqual(self.tb.main_str_descr_cd, "N")
#         self.assertEqual(self.tb.apprh_str_descr_cd, "N")
#         self.assertEqual(self.tb.hist_build_yr, "1956")
#         self.assertEqual(self.tb.nlfid, "SPICUS00023**N")
#         self.assertEqual(self.tb.ctl_begin_nbr, 3.61)
#         self.assertEqual(self.tb.route_type, "US")
#         self.assertEqual(self.tb.route_nbr, "00023")
#         self.assertEqual(self.tb.route_suffix, "*")
#         self.assertEqual(self.tb.routine_insp_due, 1738368000000)
#         self.assertEqual(self.tb.frac_crit_insp_due, None)
#         self.assertEqual(self.tb.dive_insp_due, None)
#         self.assertEqual(self.tb.spcl_insp_due, None)
#         self.assertEqual(
#             self.tb.bia_report,
#             "https://smsreports.dot.state.oh.us/CreateReport.aspx?SFN=6500609&IsBIA=true",
#         )
#         self.assertEqual(
#             self.tb.state_route_br_photos,
#             "https://brphotos.dot.state.oh.us/Bridges.aspx?county=PIC",
#         )
#         self.assertEqual(self.tb.jurisdiction, "S")
#         self.assertEqual(self.tb.divided_hwy, "N")
#         self.assertEqual(self.tb.access_control, None)
#         self.assertEqual(self.tb.urban_area_code, "99999")
#         self.assertEqual(self.tb.base_type, None)
#         self.assertEqual(self.tb.functional_class, "3")
#         self.assertEqual(self.tb.hpms_sample_id, None)
#         self.assertEqual(self.tb.lanes, None)
#         self.assertEqual(self.tb.maintenance_authority, None)
#         self.assertEqual(self.tb.nhs, "H")
#         self.assertEqual(self.tb.priority_system, None)
#         self.assertEqual(self.tb.surface_type, None)
#         self.assertEqual(self.tb.surface_width, None)
#         self.assertEqual(self.tb.esal_total, None)
#         self.assertEqual(self.tb.pave_type, "FLEX")
#         self.assertEqual(self.tb.pcr_year, None)
#         self.assertEqual(self.tb.roadway_width_nbr, None)
#         self.assertEqual(self.tb.created_user, "TIMS@P31_TIMS_CLASSIC")
#         self.assertIsInstance(self.tb.created_date, int)
#         self.assertEqual(self.tb.last_edited_user, "TIMS@P31_TIMS_CLASSIC")
#         self.assertIsInstance(self.tb.last_edited_date, int)
#
#
# # //TODO - Fix this test, unstable API
#
#
# class TestProject(unittest.TestCase):
#     def setUp(self):
#         # Creates a 'test project' and makes sure none of the attributes have changed
#         self.tp = Project(pid="112664")
#
#     def tearDown(self):
#         pass
#
#     def test_init(self):
#         # //TODO - make tests less dependent on getting specific values from project points arrays
#         self.assertIsInstance(self.tp.objectid, int)
#         self.assertIsInstance(self.tp.gis_id, int)
#         self.assertEqual(self.tp.pid_nbr, 112664)
#         self.assertEqual(self.tp.district_nbr, 6)
#         self.assertEqual(self.tp.locale_short_nme, "D06")
#         self.assertEqual(self.tp.county_nme, "District 6")
#         self.assertEqual(self.tp.project_nme, "D06-FY23 Bridge Repair")
#         self.assertEqual(self.tp.contract_type, "Standard Build")
#         self.assertEqual(
#             self.tp.primary_fund_category_txt, "District Preservation (Pv & Br)"
#         )
#         self.assertEqual(self.tp.project_manager_nme, "PARKS, DANE RICHARD")
#         self.assertEqual(self.tp.reservoir_year, None)
#         self.assertEqual(self.tp.tier, None)
#         self.assertEqual(self.tp.odot_letting, "ODOT Let")
#         self.assertEqual(self.tp.schedule_type_short_nme, "Standard")
#         self.assertEqual(self.tp.env_project_manager_nme, "GARTNER, JANICE M")
#         self.assertEqual(self.tp.area_engineer_nme, "VANCE, JEFFREY A")
#         self.assertEqual(self.tp.project_engineer_nme, "FIRIS, BENJAMIN L")
#         self.assertEqual(self.tp.design_agency, "DISTRICT 6-ENGINEERING")
#         self.assertEqual(self.tp.sponsoring_agency, "DISTRICT 6-BRIDGES")
#         self.assertEqual(self.tp.pdp_short_name, "Path 1")
#         self.assertEqual(self.tp.primary_work_category, "Bridge Preservation")
#         self.assertEqual(self.tp.project_status, "Awarded")
#         self.assertEqual(self.tp.fiscal_year, "2023")
#         self.assertEqual(self.tp.inhouse_design_full_nme, "BLOOR, CLAYTON  ")
#         self.assertEqual(self.tp.est_total_constr_cost, 469316.5)
#         self.assertEqual(self.tp.state_project_nbr, "230339")
#         self.assertEqual(self.tp.constr_vendor_nme, "EVERS STEEL CONSTRUCTION LLC")
#         self.assertEqual(self.tp.stip_flag, "N")
#         self.assertEqual(self.tp.current_stip_co_amt, None)
#         self.assertEqual(
#             self.tp.project_plans_url,
#             "http://contracts.dot.state.oh.us/search.jsp?cabinetId=1002&PID_NUM=112664",
#         )
#         self.assertEqual(
#             self.tp.project_addenda_url,
#             "http://contracts.dot.state.oh.us/search.jsp?cabinetId=1000&PID_NUM=112664",
#         )
#         self.assertEqual(
#             self.tp.project_proposal_url,
#             "http://contracts.dot.state.oh.us/search.jsp?cabinetId=1003&PID_NUM=112664",
#         )
#         self.assertEqual(self.tp.fmis_proj_desc, None)
#         self.assertEqual(self.tp.award_milestone_dt, 1685664000000)
#         self.assertEqual(self.tp.begin_constr_milestone_dt, 1688947200000)
#         self.assertEqual(self.tp.end_constr_milestone_dt, 1697328000000)
#         self.assertEqual(self.tp.open_traffic_dt, None)
#         self.assertEqual(self.tp.central_office_close_dt, None)
#         self.assertIsInstance(self.tp.source_last_updated, int)
#         self.assertIsInstance(self.tp.cod_last_updated, int)
#         self.assertEqual(self.tp.preserv_funds_ind, "Y")
#         self.assertEqual(self.tp.major_brg_funds_ind, "N")
#         self.assertEqual(self.tp.major_new_funds_ind, "N")
#         self.assertEqual(self.tp.major_rehab_funds_ind, "N")
#         self.assertEqual(self.tp.mpo_funds_ind, "N")
#         self.assertEqual(self.tp.safety_funds_ind, "N")
#         self.assertEqual(self.tp.local_funds_ind, "N")
#         self.assertEqual(self.tp.other_funds_ind, "Y")
#         self.assertEqual(self.tp.nlf_id, "SFRAIR00071**C")
#         self.assertIsInstance(self.tp.ctl_begin, float)
#         self.assertEqual(self.tp.ctl_end, None)
#         self.assertEqual(self.tp.gis_feature_type, "POINT")
#         self.assertEqual(self.tp.route_type, "IR")
#         self.assertEqual(self.tp.route_id, "00071")
#         self.assertIsInstance(self.tp.structure_file_nbr, str)
#         self.assertIsInstance(self.tp.main_structure_type, str)
#         self.assertIsInstance(self.tp.sufficiency_rating, str)
#         self.assertIsInstance(self.tp.ovrl_structure_length, float)
#         self.assertIsInstance(self.tp.deck_area, int)
#         self.assertIsInstance(self.tp.deck_width, float)
#         self.assertEqual(self.tp.feature_intersect, "WEBER RD")
#         # self.assertIsInstance(self.tp.year_built, str)
#         self.assertIsInstance(self.tp.longitude_begin_nbr, float)
#         self.assertIsInstance(self.tp.latitude_begin_nbr, float)
#         self.assertEqual(self.tp.longitude_end_nbr, None)
#         self.assertEqual(self.tp.latitude_end_nbr, None)
#         self.assertEqual(self.tp.county_cd_work_location, "FRA")
#         self.assertEqual(self.tp.county_nme_work_location, "FRANKLIN")
#         self.assertEqual(self.tp.district_work_location, "06")
#         self.assertEqual(self.tp.pavement_treatment_type, None)
#         self.assertEqual(self.tp.pavement_treatment_category, None)
#         self.assertEqual(self.tp.created_user, "TIMS@P31_TIMS_CLASSIC")
#         self.assertIsInstance(self.tp.created_date, int)
#         self.assertEqual(self.tp.last_edited_user, "TIMS@P31_TIMS_CLASSIC")
#         self.assertIsInstance(self.tp.last_edited_date, int)
#
#
# if __name__ == "__main__":
#     unittest.main()
