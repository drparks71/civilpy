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

from civilpy.structural.steel import W, MC
from civilpy.general import units
from termcolor import colored
import math


class GlobalDefinitions:
    def __init__(
        self,
        f_y=50000 * units("psi"),
        e_steel=29000000 * units("psi"),
        tie_length=8.5 * units("ft"),
        tie_width=8 * units("inch"),
        tie_depth=7 * units("inch"),
        tie_design_width=8
        * units("ft"),  # Design width for distributed loading, length
        max_tie_spacing=24 * units("inch"),  # used for dead load
        future_ballast=12 * units("inch"),
        future_ballast_quantity=1,
        tie_material="Concrete",
        tie_spacing=1.5 * units("ft"),
        railroad_gage=4 * units("ft")
        + 8.5 * units("inch"),  # //TODO - Verify: Not AREMA
        poisson_ratio=0.30,
        steel_unit_weight=490 * units("lbf/ft^3"),
        ballast_unit_weight=120 * units("lbf/ft^3"),
        tie_unit_weight=150 * units("lbf/ft^3"),
        track_unit_weight=200 * units("lbf/ft"),
        waterproofing_unit_weight=2 * units("lbf/ft^2"),
        steel_connection_contingency=0.1,
        asphalt_unit_weight=150 * units("lbf/ft^3"),
        timber_unit_weight=60 * units("lbf/ft^3"),
    ):
        self.F_y = f_y
        self.E_steel = self.E = e_steel
        self.tie_length = tie_length
        self.tie_width = tie_width
        self.tie_depth = tie_depth
        self.tie_design_width = tie_design_width
        self.max_tie_spacing = max_tie_spacing
        self.future_ballast = future_ballast
        self.future_ballast_quantity = future_ballast_quantity
        self.tie_material = tie_material
        self.tie_spacing = tie_spacing
        self.railroad_gage = railroad_gage
        self.poisson_ratio = poisson_ratio
        self.steel_unit_weight = steel_unit_weight
        self.ballast_unit_weight = ballast_unit_weight
        self.tie_unit_weight = tie_unit_weight
        self.track_unit_weight = track_unit_weight
        self.waterproofing_unit_weight = waterproofing_unit_weight
        self.steel_connection_contingency = steel_connection_contingency
        self.asphalt_unit_weight = asphalt_unit_weight
        self.timber_unit_weight = timber_unit_weight


class LoadDefinitions:
    def __init__(
        self,
        diaphragm_weight_ft=61 * units("lbf/ft"),
        diaphragm_quant=1,
        bracing_quant=4,
        ballasted_deck_reduction=0.9,
        rocking_percent=0.2,
        wind_load=300 * units("lbf/ft"),
        wind_load_h=8 * units("ft"),
        axel_load=100 * units("kips"),
        reduction_fact=0.9,
        wheel_load_percentage=0.2,
        # //TODO - Replace these values with a simpler table lookup
        e80_50_ft=1901.80 * units("kip*ft"),
        e80_55_ft=2233.10 * units("kip*ft"),
        end_diaphragm_weight_per_ft=61 * units("lbf/ft"),
        end_diaphragm_quantity=1,
        axel_alternative_live_load=100 * units("kips"),
        jack_pt_offset=3.75 * units("ft"),
    ):
        self.diaphragm_weight_ft = diaphragm_weight_ft
        self.diaphragm_quant = diaphragm_quant
        self.bracing_quant = bracing_quant
        self.ballasted_deck_reduction = ballasted_deck_reduction
        self.rocking_percent = rocking_percent
        self.wind_load = wind_load
        self.wind_load_h = wind_load_h
        self.axel_load = axel_load
        self.reduction_fact = reduction_fact
        self.wheel_load_percentage = wheel_load_percentage
        self.e80_50_ft = e80_50_ft
        self.e80_55_ft = e80_55_ft
        self.end_diaphragm_weight_per_ft = end_diaphragm_weight_per_ft
        self.end_diaphragm_quantity = end_diaphragm_quantity
        self.axel_alternative_live_load = axel_alternative_live_load
        self.jack_pt_offset = jack_pt_offset


default_fb = W("w24x250")


class ThroughPlateGirderFloorbeam:
    def __init__(
        self,
        rolled_shape=True,
        shape="W24x250",
        fb_depth=default_fb.depth,
        fb_web_thickness=default_fb.web_thickness,
        fb_i_x=default_fb.I_x,
        fb_flange_width=default_fb.flange_width,
        fb_weight=default_fb.weight,
        fb_r_y=default_fb.r_y,
        fb_flange_thickness=default_fb.flange_thickness,
        fb_bracket_flange_t=0.75 * units("inch"),
        fb_bracket_flange_web=8.0 * units("inch"),
        fb_bracket_flange_len=3.33 * units("foot"),
        fb_bracket_web_t=0.5 * units("inch"),
        fb_bracket_web_width=1.83 * units("ft"),
        fb_bracket_web_height=2.75 * units("ft"),
        fb_bracket_quantity=12,
        fb_length=20 * units("ft"),
        rr_gage=4 * units("ft") + 8.5 * units("inch"),
        A=100 * units("kip"),
        s=5 * units("ft"),
    ):
        # FB Definitions
        # //TODO - Replace the following values with rolled beam values if we usually use rolled beams
        if not rolled_shape:
            self.shape = (shape,)
            self.depth = (fb_depth,)
            self.web_thickness = (fb_web_thickness,)
            self.I_x = (fb_i_x,)
            self.flange_width = (fb_flange_width,)
            self.weight = (fb_weight,)
            self.r_y = (fb_r_y,)
            self.flange_thickness = fb_flange_thickness
        else:
            shape_obj = W(shape)
            self.depth = shape_obj.depth
            self.web_thickness = shape_obj.web_thickness
            self.I_x = shape_obj.I_x
            self.flange_width = shape_obj.flange_width
            self.weight = shape_obj.weight
            self.r_y = shape_obj.r_y
            self.flange_thickness = shape_obj.flange_thickness
        self.bracket_flange_t = fb_bracket_flange_t
        self.bracket_flange_web = fb_bracket_flange_web
        self.bracket_flange_len = fb_bracket_flange_len
        self.bracket_web_t = fb_bracket_web_t
        self.bracket_web_width = fb_bracket_web_width
        self.bracket_web_height = fb_bracket_web_height
        self.bracket_quantity = fb_bracket_quantity
        self.a = fb_length / 2 - rr_gage / 2
        self.A = A
        self.s = s


class TPG:
    def __init__(
        self,
        floorbeam_spacing=2.6 * units("ft"),
        floorbeam_quantity=19,
        end_floorbeam_quantity=2,
        # Girder Definitions
        girder_spacing=20 * units("ft"),
        girder_web_height=60 * units.inch,
        girder_web_thickness=0.625 * units.inch,
        girder_flange_width=20 * units.inch,
        girder_flange_thickness=1.625 * units.inch,
        # Diaphragm Definitions
        max_diaphragm_spacing=10.00 * units("ft"),
        diaphragm_quantity=20,
        # Hole Definitions
        diaphragm_dia_hole=1.0 * units("in"),
        diaphragm_num_holes=4,
        end_diaphragm_hole_quantity=6,
        lateral_dia_holes=1.0 * units("in"),
        lateral_num_holes=2,
        web_conn_girder_holes_num=6,
        web_conn_girder_holes_dia=1 * units("in"),
        span_length=52.00 * units("ft"),
        girder_length=54 * units("ft"),
        floor_length=58 * units("ft"),
        floor_quantity=1,
        rail_quantity=1,
        asphaltic_plank_t=1 * units("in"),
        ballast_plate_spacing=3 * units("ft"),
        asphaltic_plank_quant=1,
        # Deck plate definitions
        deck_plate_thickness=0.75 * units("in"),
        min_ballast_below_tie=6 * units("in"),
        deck_plate_width=12.00 * units("in"),
        waterproofing_quant=1,
        ballast_under_ties_t=9 * units("in"),
        ballast_under_ties_quant=1,
        tie_level_ballast_quant=1,
        tie_level_ballast_sloped_reduction=2 * units("ft^2"),
        tie_level_ballast_include_pre_move_weight=False,
        # //TODO - Verify what these diagonal/horizontal formulas/values are dependent on
        dia_stop_pl_t=0.5 * units("in"),
        dia_stop_pl_width=(
            (1 * units("ft") + 10 * units("inch")) ** 2
            + (1 * units.ft + (1 + 3 / 16) * units("inch")) ** 2
        )
        ** 0.5,
        dia_stop_pl_quantity=40,
        horizontal_upper_floor_pl_t=0.50 * units("in"),
        horizontal_upper_floor_pl_width=((1 + 10 / 12 + 13 / 16 / 12) + 3 / 12)
        * units("ft"),
        horizontal_upper_floor_pl_quantity=10,
        girder_quantity=2,
        assumed_mean_impact_perc=0.35,  # AREMA Table 15-1-8
        # Bracing Values
        bracing_section="MC10x33.6",
        lateral_bracing_length=32.8024 * units("ft"),
        lateral_bracing_quantity=4,
        # Stiffener Values
        trans_stiff_da=96 * units("in"),
        trans_stiff_actual_da=60 * units("in"),
        stiffener_width_bst=6 * units("in"),
        stiffener_thickness_tst=0.5 * units("in"),
        bearing_stiffener_thickness_tsb=1 * units("in"),
        bearing_stiffener_corner_clip=1 * units("in"),
        bearing_stiffener_fillet_weld_leg=0.3125 * units("in"),
        end_floorbeam=W("W21X166"),
        diaphragm=W("W16X89"),
        lateral_bracing=MC("MC10x33.6"),
        # Load the Load Definitions
        load_values=LoadDefinitions(),
        # Loads Global Variables (Non-bridge specific)
        global_values=GlobalDefinitions(),
        # Loads Floorbeam Variables
        floorbeam_values=ThroughPlateGirderFloorbeam(),
    ):
        self.global_defs = global_values
        self.load_values = load_values
        self.fb = floorbeam_values

        # Global Input
        self.floorbeam_spacing = floorbeam_spacing
        self.floorbeam_quantity = floorbeam_quantity
        self.end_floorbeam_quantity = end_floorbeam_quantity

        # Steel Section inputs
        self.end_floorbeam = end_floorbeam
        self.diaphragm = diaphragm
        self.lateral_bracing = lateral_bracing

        # Girder Geometrics
        self.girder_spacing = girder_spacing
        self.girder_web_height = girder_web_height
        self.girder_web_thickness = girder_web_thickness
        self.girder_flange_width = girder_flange_width
        self.girder_flange_thickness = girder_flange_thickness

        self.ballast_plate_spacing = ballast_plate_spacing
        self.max_diaphragm_spacing = max_diaphragm_spacing
        self.diaphragm_quantity = diaphragm_quantity
        self.span_length = span_length
        self.girder_length = girder_length
        self.floor_length = floor_length
        self.floor_quantity = floor_quantity
        self.rail_quantity = rail_quantity
        self.waterproofing_quant = waterproofing_quant
        self.asphaltic_plank_t = asphaltic_plank_t
        self.asphaltic_plank_quant = asphaltic_plank_quant
        self.ballast_under_ties_t = ballast_under_ties_t
        self.ballast_under_ties_quant = ballast_under_ties_quant
        self.tie_level_ballast_quant = tie_level_ballast_quant
        self.tie_level_ballast_sloped_reduction = tie_level_ballast_sloped_reduction
        self.tie_level_ballast_include_pre_move_weight = (
            tie_level_ballast_include_pre_move_weight
        )
        self.dia_stop_pl_t = dia_stop_pl_t
        self.dia_stop_pl_width = dia_stop_pl_width
        self.dia_stop_pl_quantity = dia_stop_pl_quantity
        self.horizontal_upper_floor_pl_t = horizontal_upper_floor_pl_t
        self.horizontal_upper_floor_pl_width = horizontal_upper_floor_pl_width
        self.horizontal_upper_floor_pl_quantity = horizontal_upper_floor_pl_quantity
        self.diaphragms = diaphragm.id
        self.girder_quantity = girder_quantity
        self.assumed_mean_impact_perc = assumed_mean_impact_perc

        # Section Hole definitions
        self.diaphragm_dia_hole = diaphragm_dia_hole
        self.diaphragm_num_holes = diaphragm_num_holes

        self.lateral_dia_holes = lateral_dia_holes
        self.lateral_num_holes = lateral_num_holes
        self.web_conn_girder_holes_num = web_conn_girder_holes_num
        self.web_conn_girder_holes_dia = web_conn_girder_holes_dia

        # Bracing Value Definitions
        self.bracing_section = bracing_section
        self.lateral_bracing_length = lateral_bracing_length
        self.lateral_bracing_quantity = lateral_bracing_quantity
        self.end_diaphragm_hole_quantity = end_diaphragm_hole_quantity

        # Stiffener Value Definitions
        self.trans_stiff_da = trans_stiff_da
        self.trans_stiff_actual_da = trans_stiff_actual_da
        self.stiffener_width_bst = stiffener_width_bst
        self.stiffener_thickness_tst = stiffener_thickness_tst
        self.bearing_stiffener_thickness_tsb = bearing_stiffener_thickness_tsb
        self.bearing_stiffener_corner_clip = bearing_stiffener_corner_clip
        self.bearing_stiffener_fillet_weld_leg = bearing_stiffener_fillet_weld_leg

        self.deck_plate_thickness = deck_plate_thickness
        self.min_ballast_below_tie = min_ballast_below_tie
        self.deck_plate_width = deck_plate_width
        self.ballast_plates_clear_space = girder_spacing - 2 * ballast_plate_spacing
        self.stop_plate_detail_width = (
            girder_spacing - self.ballast_plates_clear_space
        ) / 2

        if self.span_length > 30 * units("ft"):
            self.impact_factor = 0.35  # AREMA 15 - Table 15-1-8 # //TODO - Copy
        else:
            pass

        self.run_calcs()

    def run_calcs(self):
        self.L_brace = 4 * self.floorbeam_spacing
        # AREMA 15- 1.7.7.a
        self.bearing_stiffener_width_bsb = (
            self.girder_flange_width - self.girder_web_thickness
        ) / 2

        # Basic girder geometrics definitions
        self.girder_top_flange_area = (
            self.girder_flange_width * self.girder_flange_thickness
        )
        self.girder_web_area = self.girder_web_height * self.girder_web_thickness
        self.girder_bot_flange_area = (
            self.girder_flange_width * self.girder_flange_thickness
        )

        self.girder_top_flange_centroid_height = (
            self.girder_flange_thickness
            + self.girder_web_height
            + self.girder_flange_thickness / 2
        )
        self.girder_web_centroid_height = (
            self.girder_flange_thickness + self.girder_web_height / 2
        )
        self.girder_bot_flange_centroid_height = self.girder_flange_thickness / 2

        # Moment of Inertia values
        self.girder_top_flange_I_o = (
            self.girder_flange_width * self.girder_flange_thickness**3
        ) / 12
        self.girder_web_I_o = (
            self.girder_web_thickness * self.girder_web_height**3
        ) / 12
        self.girder_bot_flange_I_o = (
            self.girder_flange_width * self.girder_flange_thickness**3
        ) / 12

        # Table Values depend on the following two definitions
        self.girder_height = (
            self.girder_flange_thickness
            + self.girder_web_height
            + self.girder_flange_thickness
        )
        self.girder_centroid = self.girder_height / 2

        # Ay^2 Values in table
        self.girder_top_flange_A_y_sq = (
            self.girder_top_flange_area
            * (self.girder_top_flange_centroid_height - self.girder_centroid) ** 2
        )
        self.girder_web_A_y_sq = (
            self.girder_web_area
            * (self.girder_web_centroid_height - self.girder_centroid) ** 2
        )
        self.girder_bot_flange_A_y_sq = (
            self.girder_top_flange_area
            * (self.girder_bot_flange_centroid_height - self.girder_centroid) ** 2
        )

        # Out-of-Plane I_o
        self.girder_top_flange_oop_I_o = (
            self.girder_flange_thickness * self.girder_flange_width**3
        ) / 12
        self.girder_web_oop_I_o = (
            self.girder_web_height * self.girder_web_thickness**3 / 12
        )
        self.girder_bot_flange_oop_I_o = (
            self.girder_flange_thickness * self.girder_flange_width**3
        ) / 12

        # Remaining Girder Section Properties
        self.girder_area = (
            self.girder_top_flange_area
            + self.girder_web_area
            + self.girder_bot_flange_area
        )
        self.girder_I_xx = (
            self.girder_top_flange_I_o
            + self.girder_web_I_o
            + self.girder_bot_flange_I_o
            + self.girder_top_flange_A_y_sq
            + self.girder_web_A_y_sq
            + self.girder_bot_flange_A_y_sq
        )
        self.girder_S_xx = self.girder_I_xx / self.girder_centroid
        self.girder_r_xx = (self.girder_I_xx / self.girder_area) ** 0.5
        self.girder_I_yy = (
            self.girder_top_flange_oop_I_o
            + self.girder_web_oop_I_o
            + self.girder_bot_flange_oop_I_o
        )
        self.girder_S_yy = self.girder_I_yy / (self.girder_flange_width / 2)
        self.girder_r_yy = (self.girder_I_yy / self.girder_area) ** 0.5
        self.girder_weight_per_ft_no_cont = (
            self.girder_area * self.global_defs.steel_unit_weight
        ).to("lbf/ft")

        # No Holes
        self.girder_S_x_net = self.girder_S_xx

        #                                    # Dead Load Calculations
        # Girder Dead Loads
        self.girder_weight_per_ft = (
            self.girder_weight_per_ft_no_cont
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kip/ft")
        self.girder_self_load = (
            self.girder_area
            * self.girder_length
            * self.global_defs.steel_unit_weight
            * self.girder_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kip")

        # Intermediate Floor beams Dead Loads
        self.int_floorbeam_dl = (
            self.girder_spacing
            * self.fb.weight
            * self.floorbeam_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kips")

        # End Floor Beams Dead Loads
        self.end_floorbeam_weight = (
            self.girder_spacing
            * self.end_floorbeam.weight
            * self.end_floorbeam_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kips")

        self.total_floorbeam_weight = self.end_floorbeam_weight + self.int_floorbeam_dl

        # Diaphragms Dead Loads
        self.total_diaphragm_weight = (
            self.floorbeam_spacing
            * self.diaphragm.weight
            * self.diaphragm_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kips")

        # Lateral Bracing # //TODO - lateral bracing quantity seems low
        self.total_lateral_weight = (
            self.lateral_bracing_length
            * self.lateral_bracing.weight
            * self.lateral_bracing_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kips")

        # Floor Dead Loads
        self.deck_plate_lin_weight_per_girder = (
            self.deck_plate_thickness
            * self.ballast_plates_clear_space
            * self.global_defs.steel_unit_weight
            * (1 + self.global_defs.steel_connection_contingency)
            / 2
        ).to("lbf/ft")
        self.floor_area_load = (
            self.deck_plate_thickness
            * self.global_defs.steel_unit_weight
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("lbf/ft^2")

        self.total_floor_weight = (
            self.deck_plate_thickness
            * self.ballast_plates_clear_space
            * self.floor_length
            * self.global_defs.steel_unit_weight
            * self.floor_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kip")

        # Diagonal Stop Plate # //TODO - ask about what this detail is
        self.dia_stop_pl_lin_w_per_girder = (
            self.dia_stop_pl_t
            * self.dia_stop_pl_width
            * self.global_defs.steel_unit_weight
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("lbf/ft")
        self.dia_stop_pl_area_load = (
            self.dia_stop_pl_t
            * self.dia_stop_pl_width
            * self.global_defs.steel_unit_weight
            * (1 + self.global_defs.steel_connection_contingency)
            / self.stop_plate_detail_width
        ).to("lbf/ft^2")

        self.dia_stop_pl_weight = (
            self.dia_stop_pl_t
            * self.dia_stop_pl_width
            * self.floorbeam_spacing
            * self.global_defs.steel_unit_weight
            * self.dia_stop_pl_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kip")

        # Horizontal Upper Floor Plate # //TODO - Ask about what this detail is
        self.horizontal_upper_fl_pl_length = 4 * self.floorbeam_spacing - 8 * units(
            "in"
        )  # //TODO - is this always 8"
        # //TODO - formula given says (1+C), which is hard coded as 10.4, figure out what this is,
        # //TODO - also width has bad math in excel
        self.horizontal_upper_fl_pl_weight_per_girder = (
            self.horizontal_upper_floor_pl_t
            * self.horizontal_upper_floor_pl_width
            * self.global_defs.steel_unit_weight
            * (1 + self.global_defs.steel_connection_contingency)
            * self.horizontal_upper_fl_pl_length
            / (10.4 * units("ft"))
        ).to("lbf/ft")
        self.horizontal_upper_fl_pl_area_load = (
            self.horizontal_upper_floor_pl_t
            * self.horizontal_upper_floor_pl_width
            * self.global_defs.steel_unit_weight
            * (1 + self.global_defs.steel_connection_contingency)
            / self.stop_plate_detail_width
            * self.horizontal_upper_fl_pl_length
            / (10.4 * units("ft"))
        ).to("lbf/ft^2")

        self.horizontal_upper_fl_pl_weight = (
            self.horizontal_upper_floor_pl_t
            * self.horizontal_upper_floor_pl_width
            * self.horizontal_upper_fl_pl_length
            * self.global_defs.steel_unit_weight
            * self.horizontal_upper_floor_pl_quantity
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kip")

        self.waterproofing_width = (
            self.ballast_plates_clear_space + 2 * self.dia_stop_pl_width
        )
        self.waterproofing_length = self.floor_length
        self.waterproofing_weight_per_girder = (
            self.waterproofing_width
            * self.global_defs.waterproofing_unit_weight
            / self.girder_quantity
        )
        self.waterproofing_area_load = self.global_defs.waterproofing_unit_weight
        self.waterproofing_area_load_2 = (
            self.global_defs.waterproofing_unit_weight
            * (self.waterproofing_width - 14 * units("ft"))
            / 2
            / self.stop_plate_detail_width
        )
        self.waterproofing_weight = (
            self.waterproofing_width
            * self.waterproofing_length
            * self.global_defs.waterproofing_unit_weight
            * self.waterproofing_quant
        ).to("kips")

        # Asphaltic Plank Dead load
        # Asphaltic Plank
        self.asp_plank_width = self.waterproofing_width
        self.asp_plank_length = self.floor_length
        self.asp_lin_weight_per_girder = (
            self.asp_plank_width
            * self.asphaltic_plank_t
            * self.global_defs.asphalt_unit_weight
            / self.girder_quantity
        ).to("lbf/ft")
        self.asp_plank_area_load = (
            self.asphaltic_plank_t * self.global_defs.asphalt_unit_weight
        ).to("lbf/ft^2")
        # Between stop Plates        # //TODO - Hardcoded values
        self.asp_plank_area_load_2 = (
            self.asphaltic_plank_t
            * self.global_defs.asphalt_unit_weight
            * (self.asp_plank_width - 14 * units("ft"))
            / 2
            / self.stop_plate_detail_width
        ).to("lbf/ft^2")

        self.asp_plank_weight = (
            self.asp_plank_width
            * self.asp_plank_length
            * self.global_defs.asphalt_unit_weight
            * self.asphaltic_plank_t
            * self.asphaltic_plank_quant
        ).to("kips")

        # Flooring linear weight per girder
        self.floor_weight_per_girder = (
            self.asp_lin_weight_per_girder
            + self.waterproofing_weight_per_girder
            + self.horizontal_upper_fl_pl_weight_per_girder
            + self.dia_stop_pl_lin_w_per_girder
            + self.deck_plate_lin_weight_per_girder
        )

        # Flooring Load on FBs between stop plates and deck plate
        self.floor_load_on_fbs = (
            self.asp_plank_area_load
            + self.waterproofing_area_load
            + self.floor_area_load
        ).to("lbf/ft^2")

        # Flooring Load on FBs over stop plates
        self.floor_load_over_stop_plates = (
            self.asp_plank_area_load_2
            + self.waterproofing_area_load_2
            + self.horizontal_upper_fl_pl_area_load
            + self.dia_stop_pl_area_load
        )

        # Ballast
        # Ballast Under Ties
        self.ballast_under_ties_width = (
            self.ballast_plates_clear_space + 9 / 12 * self.ballast_under_ties_t * 2 / 2
        ).to(
            "ft"
        )  # //TODO - What is the 9/12?
        self.ballast_under_ties_length = self.floor_length
        self.ballast_volume = (
            self.ballast_under_ties_width
            * self.ballast_under_ties_t
            * self.ballast_under_ties_length
        ).to("ft^3")
        self.ballast_area_load = (
            self.ballast_under_ties_t
            * self.ballast_under_ties_width
            * self.global_defs.ballast_unit_weight
            / self.ballast_plates_clear_space
        ).to("lbf/ft^2")
        self.ballast_area_load_2 = (
            self.ballast_under_ties_t * self.global_defs.ballast_unit_weight
        ).to("lbf/ft^2")

        self.ballast_weight = (
            self.ballast_under_ties_t
            * self.ballast_under_ties_width
            * self.ballast_under_ties_length
            * self.global_defs.ballast_unit_weight
            * self.ballast_under_ties_quant
        ).to("kips")

        # Tie Dead Load
        self.tie_quantity = self.floor_length / self.global_defs.tie_spacing
        self.tie_volume = (
            self.global_defs.tie_depth
            * self.global_defs.tie_width
            * self.global_defs.tie_length
            * self.tie_quantity
        )
        self.tie_vol_per_ft = (
            self.global_defs.tie_depth
            * self.global_defs.tie_width
            * self.global_defs.tie_length
            / self.global_defs.tie_spacing
        ).to("ft^3/ft")
        self.tie_area_load = (
            self.global_defs.tie_depth
            * self.global_defs.tie_width
            * self.global_defs.tie_length
            * self.global_defs.tie_unit_weight
            * 1
            / self.global_defs.tie_spacing
            / self.ballast_plates_clear_space
        ).to("lbf / ft^2")
        self.tie_area_load_2 = (
            self.global_defs.tie_depth
            * self.global_defs.tie_width
            * self.global_defs.tie_length
            * self.global_defs.tie_unit_weight
            * 1
            / self.global_defs.tie_spacing
            / self.global_defs.tie_length
        ).to("lbf/ft^2")

        self.tie_weight = (
            self.global_defs.tie_depth
            * self.global_defs.tie_width
            * self.global_defs.tie_length
            * self.global_defs.tie_unit_weight
            * self.tie_quantity
        ).to("kips")

        # Ballast at Tie Level
        self.ballast_tie_lvl_t = self.global_defs.tie_depth
        self.ballast_tie_lvl_width = (
            self.ballast_under_ties_width + 9 / 12 * self.ballast_tie_lvl_t
        )
        self.ballast_tie_level_length = self.ballast_under_ties_length

        self.ballast_tie_lvl_vol = (
            (
                self.ballast_tie_lvl_t * self.ballast_tie_lvl_width
                - self.tie_level_ballast_sloped_reduction
            )
            * self.ballast_tie_level_length
            - self.tie_volume
        ).to("ft^3")
        self.ballast_tie_lvl_area_load = (
            (
                self.ballast_tie_lvl_t * self.ballast_tie_lvl_width
                - self.tie_vol_per_ft
                - self.tie_level_ballast_sloped_reduction
            )
            * self.global_defs.ballast_unit_weight
            / self.ballast_plates_clear_space
        ).to("lbf/ft^2")
        self.ballast_tie_lvl_area_load_2 = (
            self.ballast_tie_lvl_t
            * self.global_defs.ballast_unit_weight
            * (1 - (self.global_defs.tie_width / self.global_defs.tie_spacing))
        ).to("lbf/ft^2")

        self.ballast_tie_lvl_subtotal = (
            self.ballast_tie_lvl_t * self.ballast_tie_lvl_width
            - self.tie_level_ballast_sloped_reduction
        ).to("ft^2")

        self.ballast_tie_level_weight = (
            (
                (
                    self.ballast_tie_lvl_t * self.ballast_tie_lvl_width
                    - self.tie_level_ballast_sloped_reduction
                )
                * self.ballast_tie_level_length
                - self.tie_volume
            )
            * self.global_defs.ballast_unit_weight
            * self.tie_level_ballast_quant
        ).to("kip")

        # Rail Dead Load
        self.rail_area_load = (
            self.global_defs.track_unit_weight / self.ballast_plates_clear_space
        )

        # (track_unit_weight / tie_length).to('lbf/ft^2')
        # //TODO - Don't think this is calculating correctly replaced tie width w/ tie length to be closer to same value
        self.rail_area_load_2 = 25 * units("lbf/ft^2")

        self.rail_weight = (
            self.global_defs.track_unit_weight * self.floor_length * self.rail_quantity
        ).to("kip")

        # Future ballast Allowance/Dead Load

        self.future_ballast_width = self.ballast_plates_clear_space + 9 / 12 * (
            self.ballast_under_ties_t + self.global_defs.future_ballast
        )

        self.future_ballast_vol = (
            self.global_defs.future_ballast
            * self.future_ballast_width
            * self.ballast_tie_level_length
        ).to("ft^3")
        self.future_ballast_area_load = (
            self.global_defs.future_ballast
            * self.future_ballast_width
            * self.global_defs.ballast_unit_weight
            / self.ballast_plates_clear_space
        ).to("lbf/ft^2")

        self.future_ballast_area_load_2 = (
            self.global_defs.future_ballast * self.global_defs.ballast_unit_weight
        ).to("lbf/ft^2")

        self.future_ballast_weight = (
            self.future_ballast_vol
            * self.global_defs.ballast_unit_weight
            * self.global_defs.future_ballast_quantity
        ).to("kip")

        # Summary Calcs
        self.track_weight_per_girder = (
            self.ballast_weight
            + self.tie_weight
            + self.ballast_tie_level_weight
            + self.rail_weight
            + self.future_ballast_weight
        ) / self.ballast_tie_level_length
        self.track_area_load_on_fbs = sum(
            [
                self.ballast_area_load,
                self.tie_area_load,
                self.ballast_tie_lvl_area_load,
                self.rail_area_load,
                self.future_ballast_area_load,
            ]
        )

        self.track_assembly_load_on_deck_plate = sum(
            [
                self.ballast_area_load_2,
                self.tie_area_load_2,
                self.ballast_tie_lvl_area_load_2,
                self.rail_area_load_2,
                self.future_ballast_area_load_2,
            ]
        ).to("lbf/ft^2")

        self.fb_bracket_vol = (
            self.fb.bracket_flange_t
            * self.fb.bracket_flange_web
            * self.fb.bracket_flange_len
            + self.fb.bracket_web_t
            * self.fb.bracket_web_width
            * self.fb.bracket_web_height
        ).to("ft^3")

        self.floorbeam_bracket_weight = (
            (
                self.fb_bracket_vol
                * self.global_defs.steel_unit_weight
                * self.fb.bracket_quantity
            )
            * (1 + self.global_defs.steel_connection_contingency)
        ).to("kip")

        self.list_of_dead_load_factors = [
            self.floorbeam_bracket_weight,
            self.future_ballast_weight,
            self.rail_weight,
            self.ballast_tie_level_weight,
            self.tie_weight,
            self.ballast_weight,
            self.asp_plank_weight,
            self.waterproofing_weight,
            self.horizontal_upper_fl_pl_weight,
            self.dia_stop_pl_weight,
            self.total_floor_weight,
            self.total_lateral_weight,
            self.total_diaphragm_weight,
            self.total_floorbeam_weight,
            self.girder_self_load,
        ]

        self.lifting_dead_load_factors = [
            self.floorbeam_bracket_weight,
            self.rail_weight,
            self.tie_weight,
            self.ballast_weight,  # //TODO - Shouldn't this not be included here?
            self.asp_plank_weight,
            self.waterproofing_weight,
            self.horizontal_upper_fl_pl_weight,
            self.dia_stop_pl_weight,
            self.total_floor_weight,
            self.total_lateral_weight,
            self.total_diaphragm_weight,
            self.total_floorbeam_weight,
            self.girder_self_load,
        ]

        # Calculate the Bridges Deadloads
        self.total_dead_load = sum(self.list_of_dead_load_factors)
        self.total_dead_load_lifting = sum(self.lifting_dead_load_factors)

        self.distributed_load = (
            self.total_dead_load / self.span_length / self.girder_quantity
        )

        # Girder Calcs and Checks
        self.floorbeam_load_on_girder = (
            self.total_floorbeam_weight / self.girder_quantity / self.span_length
        )
        self.diaphragm_load_on_girder = (
            self.total_diaphragm_weight / self.girder_quantity / self.span_length
        )

        self.lat_bracing_load_on_girder = (
            self.total_lateral_weight / self.girder_quantity / self.span_length
        )

        self.track_assembly = self.track_weight_per_girder
        self.total_dl_over_total_length = sum(
            [
                self.girder_weight_per_ft,
                self.floorbeam_load_on_girder,
                self.diaphragm_load_on_girder,
                self.floor_weight_per_girder,
                self.lat_bracing_load_on_girder,
                self.track_assembly,
            ]
        )

        self.w = self.total_dl_over_total_length
        self.L = self.span_length

        self.M_dl = (self.w * self.L**2 / 8).to("kips*ft")

        # //TODO - Values are hardcoded
        self.span_live_load = (
            self.load_values.e80_55_ft - self.load_values.e80_50_ft
        ) / (55 * units.ft - 50 * units.ft) * (
            self.span_length - 50 * units.ft
        ) + self.load_values.e80_50_ft
        self.M_ll = self.span_live_load

        # Impact Load      AREMA 15.1.3.5.d
        # //TODO - Hardcoded Values, make sure they match AREMA Formula
        self.impact_percent = (
            40 - 3 * self.span_length**2 / (1600 * units("ft^2"))
        ) / 100

        # //TODO - Dimensionality off, /100 should adjustment probably be in the percentage calc
        self.M_i = (
            self.M_ll * self.load_values.ballasted_deck_reduction * self.impact_percent
        )

        # Rocking Effect    AREMA 15.1.3.5.d
        self.eqiv_uniform_live_load = 8 * self.M_ll / self.span_length**2

        self.P = self.eqiv_uniform_live_load * self.load_values.rocking_percent

        self.a = (self.girder_spacing - self.global_defs.railroad_gage) / 2

        self.load_on_girder_rocking = self.P * (1 - 2 * self.a / self.girder_spacing)

        self.M_re = self.load_on_girder_rocking * self.L**2 / 8

        # Centrifugal Force    AREMA 15-1.3.6
        # //TODO - Hardcoded Values, should be inputs
        self.design_speed = 35 * units("miles/hour")

        # //TODO - Hardcoded Values, should be inputs
        self.curve_radius = 2000 * units("ft")

        # //TODO - Find a better way to handle units
        self.deg_curve = (
            2 * math.atan(100 / (2 * self.curve_radius.magnitude)) * units("rad")
        )
        self.centrifugal_percentage = 0.00117 * self.design_speed ** (
            2 * self.deg_curve
        )

        # Wind Load    # AREMA 15-1.3.7
        self.wind_load_8_ft_offset = 300 * units("lbf/ft")
        self.P = (
            8
            * units("ft")
            * self.wind_load_8_ft_offset
            / self.global_defs.railroad_gage
        )
        self.a = (self.girder_spacing - self.global_defs.railroad_gage) / 2

        self.girder_reaction_from_wind = (
            self.P * (1 - 2 * self.a / self.girder_spacing)
        ).to("kip/ft")

        self.V_wind = self.girder_reaction_from_wind * self.span_length / 2
        self.M_wind = self.girder_reaction_from_wind * self.span_length**2 / 8

        # Case 1 = M_dl + M_ll + M_i + M_re
        self.case_1 = sum([self.M_dl, self.M_ll, self.M_i, self.M_re])

        # Case 2 = (M_dl + M_ll + M_i + M_wind) / 1.25
        self.case_2 = sum([self.M_dl, self.M_ll, self.M_i, self.M_wind]) / 1.25

        self.M_tot = max(self.case_1, self.case_2)

        # Req. Section Modulus
        self.F_b = (0.55 * self.global_defs.F_y).to("kips/in^2")
        self.S_req_moment = (self.M_tot / self.F_b).to("in^3")

        # Fatigue Section Required
        # AREMA 15 - Table 15-1-7, Table 15-1-8
        self.M_if = self.M_i * self.impact_percent
        self.M_f = self.M_ll + self.M_if

        self.F_b_fat = 16 * units("ksi")  # AREMA 15 - Table 15-1-10

        self.S_req_fat = (self.M_f / self.F_b_fat).to("in^3")

        # Required Section Modulus
        self.S_req = max(self.S_req_moment, self.S_req_fat)

        # Deflection requirements for member sizing
        # AREMA 15-1.2.5b
        self.delta_max = (self.span_length / 640).to("inch")

        self.M_ll_and_M_i = self.M_ll + self.M_i

        self.w_deflection = (self.M_ll_and_M_i * 8 / self.span_length**2).to("kip/in")

        self.I_x_req = (
            5
            * self.w_deflection
            * self.span_length**4
            / (384 * self.global_defs.E_steel * self.delta_max)
        ).to("in^4")

        #                # AREMA Requirements Checks
        # Flange Compression Check
        if (self.L_brace / self.girder_r_yy) <= 5.55 * (
            self.global_defs.E_steel / self.global_defs.F_y
        ) ** 0.5:
            print(colored("Flange Compression Check - OK", "green"))
        else:
            print(colored("No Good - Compression Flange Check Failed", "red"))

        # Web Thickness     AREMA 15-1.7.3
        # Web Thickness Check 1
        if (
            self.girder_web_thickness
            >= 0.18
            * (self.global_defs.F_y / self.global_defs.E) ** 0.5
            * self.girder_web_height
        ):
            print(colored("Web Thickness Check 1 - OK", "green"))
        else:
            print(colored("No Good - Web Compression Check Failed", "red"))

        # Web Thickness Check 2
        if self.girder_web_thickness >= self.girder_flange_thickness / 6:
            print(colored("Web Thickness CHeck 2 - OK", "green"))
        else:
            print(colored("No Good - Web Compression Check Failed", "red"))

        # Outstanding Elements in Compression (AREMA 15-1.6.2)
        # Flange_compression
        if (
            self.girder_flange_width / 2
            <= 0.43
            * self.girder_flange_thickness
            * (self.global_defs.E / self.global_defs.F_y) ** 0.5
        ):
            print(colored("Flange Compression Check - OK", "green"))
        else:
            print(colored("No Good - Compression Flange Check Failed", "red"))

        # Allowable Stress
        # AREMA Table 15-1-12
        self.F_b_ten = 0.55 * self.global_defs.F_y
        self.comp_value_1 = (
            0.55 * self.global_defs.F_y
            - (
                (0.55 * self.global_defs.F_y**2)
                / (6.3 * math.pi**2 * self.global_defs.E_steel)
            )
            * (self.L_brace / self.girder_r_yy) ** 2
        )

        self.girder_depth = self.girder_web_height + 2 * self.girder_flange_thickness
        self.girder_flange_area = (
            self.girder_flange_width * self.girder_flange_thickness
        )

        self.comp_value_2 = (
            (0.131 * math.pi * self.global_defs.E_steel)
            / (
                (
                    self.L_brace
                    * self.girder_depth
                    * (1 + self.global_defs.poisson_ratio) ** 0.5
                )
                / self.girder_flange_area
            )
        ).to("psi")

        self.comp_value_3 = 0.55 * self.global_defs.F_y

        self.F_b_comp = min(
            self.comp_value_3, max(self.comp_value_2, self.comp_value_1)
        )

        # Stress in Extreme fibers of Girder
        self.F_b_comp_act = (self.M_tot / self.girder_S_xx).to("lbf/in^2")

        # Bending Check
        if self.F_b_comp_act <= self.F_b_comp:
            print(
                colored(
                    f"Bending Check - OK, Stress Ratio: {self.F_b_comp_act / self.F_b_comp}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Girder Bending Check Failed", "red"))

        self.F_b_ten_act = (self.M_tot / self.girder_S_xx).to("psi")

        # Bending Check
        if self.F_b_ten_act <= self.F_b_ten:
            print(
                colored(
                    f"Bending Check - OK, Stress Ratio: {self.F_b_ten_act / self.F_b_ten}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Girder Bending Check Failed", "red"))

        # Fatigue (AREMA 15-1.3.13)
        self.S_r_fat_actual = (self.M_f / self.girder_S_xx).to("psi")

        self.S_r_fat = self.F_b_fat.to("psi")

        # Bending Fatigue
        if self.S_r_fat_actual <= self.S_r_fat:
            print(
                colored(
                    f"Bending Fatigue - OK, Stress Ratio: {self.S_r_fat_actual / self.S_r_fat}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Girder Bending Fatigue Check Failed", "red"))

        # Deflection AREMA 15-1.2.5
        self.w = (self.M_ll + self.M_i) / (self.span_length**2) * 8

        self.delta_total = (
            (5 * self.w * (self.span_length**4))
            / (384 * self.global_defs.E_steel * self.girder_I_xx)
        ).to("in")

        # Deflection # //TODO - Not sure the ratio matters as much for this one
        if self.delta_total <= self.delta_max:
            print(
                colored(
                    f"Deflection Check - OK, Ratio: {self.delta_total / self.delta_max}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Deflection Check Failed", "red"))

        # Dead Load Camber
        self.w_dl = self.total_dl_over_total_length.to("kip/in")
        self.delta_dl = (self.delta_total * self.w_dl / self.w).to("in")

        # Web Shear
        self.V_dl = (self.w_dl * self.span_length / 2).to("kip")

        # Shear from AREMA 15 Table 1-16
        self.shear_50_ft = 174.4 * units("kips")
        self.shear_55_ft = 185.31 * units("kips")
        self.V_ll = (self.shear_55_ft - self.shear_50_ft) / (
            55 * units("ft") - 50 * units("ft")
        ) * (self.span_length - 50 * units("ft")) + self.shear_50_ft

        self.V_imp = 0.9 * self.V_ll * self.impact_percent  # AREMA 15-1.3.5.b

        self.R1_rocking_force = self.load_on_girder_rocking
        self.V_re = self.R1_rocking_force * self.L / 2

        self.V_tot = self.V_dl + self.V_ll + self.V_re + self.V_imp

        self.F_r = self.V_tot / (self.girder_web_height * self.girder_web_thickness)

        self.F_v = (0.35 * self.global_defs.F_y).to("kips/in^2")

        # Web Shear AREMA Table 15-1-12 check #
        # // TODO - This Check isn't comparing like units in the excel sheet?, think it should be as follows,
        if self.F_r <= self.F_v:
            print(
                colored(
                    f"Web Shear Check - OK, Stress Ratio: {self.F_r / self.F_v}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Web Shear Check Failed", "red"))

        # Allowable Stress on welds
        self.Q = (
            self.girder_flange_width
            * self.girder_flange_thickness
            * (self.girder_web_height / 2 + self.girder_flange_thickness / 2)
        )
        self.F_r = self.V_tot * self.Q / (self.girder_I_xx * self.girder_web_thickness)

        # Weld Strength
        if self.F_r <= self.F_v:
            print(
                colored(
                    f"Weld Strength Check - OK, Stress Ratio: {self.F_r / self.F_v}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Weld Strength Check Failed", "red"))

        # Web plate stiffeners
        # AREMA 15-1.7.8.a
        self.trans_stiff_check = (
            2.12
            * (self.global_defs.E_steel / self.global_defs.F_y) ** 0.5
            * self.girder_web_thickness
        )

        # Transverse stiffener check
        if self.trans_stiff_check <= self.girder_web_height:
            print(colored("Transverse Stiffeners Required", "red"))
        else:
            print(colored("Transverse Stiffeners NOT Required", "green"))

        # //TODO - Look into this value, it's not used
        self.clear_dist_to_prev_web_shear_buck = (
            1.95 * (self.global_defs.E_steel * self.girder_S_xx) ** 0.5
        )

        self.Q = (
            self.girder_flange_width
            * self.girder_flange_thickness
            * (self.girder_web_height + self.girder_flange_thickness)
            / 2
            + self.girder_web_height
            * self.girder_web_thickness
            / 2
            * self.girder_web_height
            / 4
        )

        self.S = self.f_v = (
            self.V_tot * self.Q / (self.girder_I_xx * self.girder_web_thickness)
        )

        self.d = (
            1.95
            * self.girder_web_thickness
            * (self.global_defs.E_steel / self.S) ** 0.5
        )

        self.max_clear_dist = min([self.d, self.trans_stiff_da, self.girder_web_height])

        # Weld Strength
        if (
            self.trans_stiff_actual_da <= self.max_clear_dist
            or self.girder_web_height <= self.trans_stiff_check
        ):
            print(colored("Weld Strength Check - OK", "green"))
        else:
            print(colored("No Good - Stiffener Spacing Check Failed", "red"))

        self.D_d = max(1, min(5, self.girder_web_height / self.d))

        # Required Moment of inertia (Stiffener) AREMA 15-1.7.8.a
        self.stiff_I_xx_req = (
            2.5
            * self.trans_stiff_actual_da
            * self.girder_web_thickness**3
            * (self.D_d**2 - 0.7)
        )

        self.stiff_I_xx_act = (
            self.stiffener_thickness_tst * self.stiffener_width_bst**3 / 12
            + self.stiffener_thickness_tst
            * self.stiffener_width_bst
            * (self.girder_web_thickness / 2 + self.stiffener_width_bst / 2) ** 2
        )

        # Stiffener I_xx Check
        if (
            self.stiff_I_xx_act >= self.stiff_I_xx_req
            or self.girder_web_height <= self.trans_stiff_check
        ):
            print(colored("Stiffener I_xx Check - OK", "green"))
        else:
            print(colored("No Good - Stiffener Spacing Check Failed", "red"))

        # Max Stiffener Width AREMA 15-1.7.8.b
        self.max_stiff_width = 16 * self.stiffener_thickness_tst
        self.min_stiff_width = 2 * units("in") + self.girder_height / 30

        self.stiff_t_check_1 = (
            self.max_stiff_width >= self.stiffener_width_bst >= self.min_stiff_width
        )
        self.stiff_t_check_2 = self.girder_web_height <= self.trans_stiff_check

        # Stiffener Thickness Check
        if self.stiff_t_check_1 or self.stiff_t_check_2:
            print(colored("Stiffener Thickness Check - OK", "green"))
        else:
            print(colored("No Good - Stiffener Thickness Check Failed", "red"))

        # Transverse Stiffener Weld Fatigue Stress
        self.d = self.girder_web_height / 2
        self.S_stiff = self.girder_I_xx / self.d
        self.sr_weld = (self.M_f / self.S_stiff).to("psi")

        self.F_b_fat_trans = 12000 * units(
            "psi"
        )  # Stress category C' N>2,000,000 cycles AREMA 15-1-9

        # Stiffener Weld Fatigue
        if self.sr_weld <= self.F_b_fat_trans:
            print(
                colored(
                    f"Stiffener Weld Fatigue - OK, Stress Ratio: {self.sr_weld / self.F_b_fat_trans}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Stiffener Weld Fatigue Check Failed", "red"))

        # Longitudinal Plate Stiffeners
        # AREMA 15-1.7.8.f

        # Longitudinal Stiffeners
        if (
            self.girder_web_height
            <= 4.18
            * (self.global_defs.E_steel / self.global_defs.F_y) ** 0.5
            * self.girder_web_thickness
        ):
            self.long_stiff_check = "Not Required"
            print(colored("Longitudinal Stiffeners not required", "green"))
        else:
            print(colored("Longitudinal Stiffeners Required", "red"))

        # Longitudinal Stiffeners   # //TODO - Bad Check
        if self.long_stiff_check == "Not Required":
            print(colored("Longitudinal Stiffeners Check - OK", "green"))
        else:
            print(colored("No Good - Longitudinal Stiffeners Check", "red"))

        # Bearing Stiffener
        self.bearing_stiff_limiting_ratio = (
            0.43
            * self.bearing_stiffener_thickness_tsb
            * ((self.global_defs.E_steel / self.global_defs.F_y) ** 0.5)
        ).to("in")

        # Longitudinal Stiffeners   # //TODO - Bad Check
        if self.bearing_stiffener_width_bsb <= self.bearing_stiff_limiting_ratio:
            print(colored("Longitudinal Stiffeners Check - OK", "green"))
        else:
            print(colored("No Good - Bearing Stiffeners w/t ratio Check", "red"))

        # Outstanding element in compression check
        self.effective_web_length = 25 * self.girder_web_thickness  # AREMA 15-1.7.7.c

        self.bearing_stiff_area = (
            self.girder_web_thickness * self.effective_web_length
            + 2
            * self.bearing_stiffener_width_bsb
            * self.bearing_stiffener_thickness_tsb
        )
        self.I_xx_web = (
            2
            * (
                self.bearing_stiffener_width_bsb**3
                * self.bearing_stiffener_thickness_tsb
                / 12
                + self.bearing_stiffener_width_bsb
                * self.bearing_stiffener_thickness_tsb
                * (self.girder_web_thickness / 2 + self.bearing_stiffener_width_bsb / 2)
                ** 2
            )
            + self.girder_web_thickness**3 * self.effective_web_length / 12
        )
        self.I_xx_stiff = (
            2
            * self.bearing_stiffener_thickness_tsb**3
            * self.bearing_stiffener_width_bsb
            / 12
            + self.effective_web_length**3 * self.girder_web_thickness / 12
        )

        self.controlling_moment_of_inertia = min(self.I_xx_web, self.I_xx_stiff)

        # AREMA 15-1.7.7-c
        self.effective_length = 0.75 * self.girder_web_height
        self.bear_stiff_r_y = (
            self.controlling_moment_of_inertia / self.bearing_stiff_area
        ) ** 0.5

        self.bear_stiff_slenderness_ratio = self.effective_length / self.bear_stiff_r_y

        # AREMA Table 15-1-12
        self.case_1_all_stress = 0.55 * self.global_defs.F_y
        self.case_2_all_stress = (
            0.6 * self.global_defs.F_y.magnitude
            - (17500 * self.global_defs.F_y / self.global_defs.E_steel) ** (3 / 2)
            * self.bear_stiff_slenderness_ratio
        ) * units("psi")
        self.case_3_all_stress = (
            0.514
            * math.pi**2
            * self.global_defs.E_steel
            / self.bear_stiff_slenderness_ratio**2
        )

        # Controlling Case
        if (
            self.bear_stiff_slenderness_ratio
            <= 0.629 / (self.global_defs.F_y / self.global_defs.E) ** 0.5
        ):
            print(colored("Case 1 Controls", "green"))
            self.bearing_stiff_F_a = self.case_1_all_stress
            print(f"bearing stiffener stress: {self.bearing_stiff_F_a}")
        elif (
            self.bear_stiff_slenderness_ratio
            <= 5.034 / (self.global_defs.F_y / self.global_defs.E) ** 0.5
        ):
            print(colored("Case 2 Controls", "green"))
            self.bearing_stiff_F_a = self.case_2_all_stress
            print(f"Bearing stiffener stress: {self.bearing_stiff_F_a}")
        else:
            print(colored("Case 3 Controls", "green"))
            self.bearing_stiff_F_a = self.case_3_all_stress
            print(f"Bearing stiffener stress: {self.bearing_stiff_F_a}")

        self.bearing_stress_act = (self.V_tot / self.bearing_stiff_area).to("psi")

        # Longitudinal Stiffeners
        if self.bearing_stress_act <= self.bearing_stiff_F_a:
            print(
                colored(
                    f"Longitudinal Stiffeners Check - OK, Stress Ratio: {self.bearing_stress_act / self.bearing_stiff_F_a}",
                    "green",
                )
            )
        else:
            print(colored("No Good - End Bearing Compression Check", "red"))

        # Bearing Stiff Weld      AREMA 15-1.7.7.a
        self.fillet_weld_area = (
            4
            * 0.707
            * self.bearing_stiffener_fillet_weld_leg
            * (self.girder_web_height - 2 * self.bearing_stiffener_corner_clip)
        )

        self.weld_stress_act = (self.V_tot / self.fillet_weld_area).to("psi")

        self.allowable_weld_stress = min(
            19000 * units("psi"), 0.35 * self.global_defs.F_y
        )  # AREMA Table 15-1-14

        # Bearing Stiff Weld Check
        if self.weld_stress_act <= self.allowable_weld_stress:
            print(
                colored(
                    f"Bearing Stiffener Weld Check - OK, Stress Ratio: {self.weld_stress_act / self.allowable_weld_stress}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Bearing Stiff Weld Check", "red"))

        # Bearing Stiff bearing area
        self.stiff_bearing_area = (
            2
            * self.bearing_stiffener_thickness_tsb
            * (
                self.bearing_stiffener_width_bsb
                - 2 * self.bearing_stiffener_corner_clip
            )
        )

        self.bearing_area_stress_act = (self.V_tot / self.stiff_bearing_area).to("psi")
        self.bearing_area_stress_all = (0.83 * self.global_defs.F_y).to("psi")

        # Bearing area allowable stress
        if self.bearing_area_stress_act <= self.bearing_area_stress_all:
            print(
                colored(
                    f"Bearing Area Allowable Stress Check - OK, Stress Ratio: {self.bearing_area_stress_act / self.bearing_area_stress_all}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Bearing Stiff Weld Check", "red"))

        # Diaphragms
        self.diaphragm.weight = 61 * units(
            "lbf/ft"
        )  # //TODO - Doesn't match section: W16x89
        self.diaphragm_quantity = 1  # //TODO - Why is this only 1 in excel?

        self.diaphragm_length = self.floorbeam_spacing

        self.lateral_bracing_length = 8.20 * units(
            "ft"
        )  # //TODO - why is this redefined and lower

        self.diaphragm_P = (
            self.diaphragm.weight * self.diaphragm_quantity * self.diaphragm_length
        )
        self.bracing_P = (
            self.lateral_bracing.weight
            * self.load_values.bracing_quant
            * self.lateral_bracing_length
        )

        self.floorbeam_dl_V = (self.fb.weight * self.girder_spacing) / 2
        self.floorbeam_dl_M = self.fb.weight * self.girder_spacing**2 / 8

        self.diaphragm_dl_V = self.diaphragm_P / 2
        self.diaphragm_dl_M = self.diaphragm_P * self.girder_spacing / 4

        self.lateral_bracing_V = self.bracing_P / 2
        self.lateral_bracing_M = self.bracing_P * self.girder_spacing / 4

        # Floor assembly between stop plates
        self.floor_assembly_V = (
            self.ballast_plates_clear_space
            * self.floor_load_on_fbs
            * self.floorbeam_spacing
            / 2
        )
        self.floor_assembly_M = (
            (
                self.floor_load_on_fbs
                * self.floorbeam_spacing
                * self.ballast_plates_clear_space
            )
            / 4
            * (self.girder_spacing - self.ballast_plates_clear_space / 2)
        )

        # Floor assembly over stop plates
        self.fb_applied_width = (
            self.girder_spacing - self.ballast_plates_clear_space
        ) / 2

        self.floor_over_stop_pl_V = (
            self.floor_load_over_stop_plates
            * self.fb_applied_width
            * self.floorbeam_spacing
        )
        self.floor_over_stop_pl_M = (
            self.floor_load_over_stop_plates
            * self.fb_applied_width**2
            / 2
            * self.floorbeam_spacing
        )

        # Track assembly weight
        self.track_area_load_V = (
            self.track_area_load_on_fbs
            * self.ballast_plates_clear_space
            / 2
            * self.floorbeam_spacing
        )
        self.track_area_load_M = (
            self.track_area_load_on_fbs
            * self.ballast_plates_clear_space
            / 4
            * (self.girder_spacing - self.ballast_plates_clear_space / 2)
            * self.floorbeam_spacing
        )

        self.total_fb_dl_shear = sum(
            [
                self.floorbeam_dl_V,
                self.diaphragm_dl_V,
                self.lateral_bracing_V,
                self.floor_assembly_V,
                self.floor_over_stop_pl_V,
                self.track_area_load_V,
            ]
        )

        self.total_fb_dl_moment = sum(
            [
                self.floorbeam_dl_M,
                self.diaphragm_dl_M,
                self.lateral_bracing_M,
                self.floor_assembly_M,
                self.floor_over_stop_pl_M,
                self.track_area_load_M,
            ]
        )

        # Live Load
        # AREMA 15-1.3.4.2.3 Alternative live load axel
        self.fb_P_ll = 1.15 * self.fb.A * self.floorbeam_spacing / self.fb.s
        self.fb_P_2_ll = self.fb_P_ll / 2

        self.fb_V_ll = self.fb_P_2_ll
        self.fb_M_ll = self.fb_P_ll * self.fb.a / 2

        # Impact Live Load
        self.fb_impact_ll_percent = (
            40 - 3 * self.girder_spacing.magnitude**2 / 1600
        ) / 100

        self.fb_P_imp_ll = (
            self.fb_impact_ll_percent
            * self.fb_P_2_ll
            * self.load_values.ballasted_deck_reduction
        )

        self.fb_M_imp = self.fb_P_imp_ll * self.fb.a

        # Rocking Load  AREMA 1.3.5.d
        self.R1_rocking = (
            self.fb_P_2_ll
            * self.load_values.rocking_percent
            * (1 - 2 * self.a / self.girder_spacing)
        )

        self.fb_M_re = self.R1_rocking * self.a

        # Wind Force on Loaded Bridge
        self.wind_load = 300 * units("lbf/ft")
        self.fb_pws = (
            self.wind_load
            * self.load_values.wind_load_h
            * self.floorbeam_spacing
            / self.global_defs.railroad_gage
        )

        self.fb_wind_R1 = self.fb_pws * (1 - 2 * self.a / self.girder_spacing)

        self.M_wl = self.fb_wind_R1 * self.fb.a

        # Required Section Properties  # AREMA Table 15-1-11
        self.fb_M_tot_1 = sum(
            [self.total_fb_dl_moment, self.fb_M_ll, self.fb_M_imp, self.M_re]
        )
        self.fb_M_tot_2 = (
            sum(
                [
                    self.total_fb_dl_moment,
                    self.fb_M_ll,
                    self.fb_M_imp,
                    self.M_re,
                    self.M_wl,
                ]
            )
            / 1.25
        )
        self.fb_M_tot = max(self.fb_M_tot_1, self.fb_M_tot_2)

        self.fb_S_x_req = (self.fb_M_tot / (0.55 * self.global_defs.F_y)).to("in^3")

        # Holes - Assume 4 x 1" holes in web for diaphragm
        self.D1 = 3 * units("in")  # //TODO - is this a constant?
        self.D2 = 3 * units("in") + self.D1

        self.I_holes_web = (
            self.diaphragm_num_holes
            / 2
            * (self.diaphragm_dia_hole * self.fb.web_thickness)
            * self.D1**2
        ) + (
            self.diaphragm_num_holes
            / 2
            * (self.diaphragm_dia_hole * self.fb.web_thickness)
            * self.D2**2
        )

        self.I_holes_flange = (
            self.lateral_num_holes
            * self.lateral_dia_holes
            * self.fb.flange_thickness
            * (self.fb.depth / 2 - self.fb.flange_thickness / 2) ** 2
        )

        self.I_net = self.fb.I_x - self.I_holes_web - self.I_holes_flange

        self.S_x_net = self.I_net / (self.fb.depth / 2)

        # Allowable Stress (AREMA Table 15-1-12)
        self.Fb_ten = 0.55 * self.global_defs.F_y

        # Compression in extreme fiber
        self.Fb_comp_1 = (
            0.55 * self.global_defs.F_y
            - (
                0.55
                * self.global_defs.F_y**2
                / (6.3 * math.pi**2 * self.global_defs.E_steel)
            )
            * (self.max_diaphragm_spacing / self.fb.r_y) ** 2
        )
        self.Fb_comp_2 = (
            0.131
            * math.pi
            * self.global_defs.E_steel
            / (
                self.max_diaphragm_spacing
                * self.fb.depth
                * (1 + self.global_defs.poisson_ratio) ** 0.5
                / (self.fb.flange_thickness * self.fb.flange_width)
            )
        ).to("psi")
        self.Fb_comp_3 = 0.55 * self.global_defs.F_y

        self.F_b_comp = (min(self.Fb_comp_3, max(self.Fb_comp_1, self.Fb_comp_2))).to(
            "ksi"
        )

        self.f_b_act = (self.fb_M_tot / self.S_x_net).to("ksi")

        # Bearing area allowable stress
        if self.f_b_act < self.F_b_comp:
            print(
                colored(
                    f"Bearing Area Allowable Stress Check - OK, Stress Ratio: {self.f_b_act / self.F_b_comp}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam Allowable Stress Check", "red"))

        # End Shear
        self.R_dl = self.total_fb_dl_shear
        self.R_ll = self.fb_P_ll
        self.R_imp = self.fb_P_imp_ll * 2
        self.R_re = self.R1_rocking
        self.R_wl = self.fb_wind_R1

        self.R_tot = sum([self.R_dl, self.R_ll, self.R_imp, self.R_re, self.R_wl])

        # Assume 6x1" dia holes in web to connect to girder
        self.fs_net = (
            self.R_tot
            / (
                (
                    self.fb.depth
                    - self.web_conn_girder_holes_num * self.web_conn_girder_holes_dia
                )
                * self.fb.web_thickness
            )
        ).to("ksi")

        self.F_v = (0.35 * self.global_defs.F_y).to("ksi")

        # Bearing area allowable stress
        if self.fs_net < self.F_v:
            print(
                colored(
                    f"Bearing Area Allowable Stress Check - OK, Stress Ratio: {self.fs_net / self.F_v}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam End Shear Check", "red"))

        # Bolted Connection - Checked in sep. calc, they account for combined effect so no 1.25 increase
        # AREMA 15 1.5.9.a.1 # //TODO - Investigate this standard

        # Floor beam fatigue
        self.fb_fat_imp_M = self.assumed_mean_impact_perc * self.fb_M_imp
        self.fb_M_fat = self.fb_M_ll + self.fb_fat_imp_M

        self.fb_live_load_stress_range = (self.fb_M_fat / self.S_x_net).to("ksi")

        # N >= 2,000,000 Category B Table 15-1-10 Detail 2.2
        self.fb_fsr = 16 * units("ksi")

        # Bearing area allowable stress
        if self.fb_live_load_stress_range < self.fb_fsr:
            print(
                colored(
                    f"Bearing Area Allowable Stress Check - OK, Stress Ratio: {self.fb_live_load_stress_range / self.fb_fsr}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam Fatigue Check", "red"))

        # Deflection
        self.fb_defl_M = self.fb_M_ll + self.fb_M_imp + self.fb_M_re

        self.fb_w = 8 * self.fb_defl_M / (self.girder_spacing**2)

        self.fb_deflection = (
            (5 * self.fb_w * self.girder_spacing**4)
            / (384 * self.global_defs.E_steel * self.fb.I_x)
        ).to("in")
        self.max_deflection = (self.girder_spacing / 640).to("in")

        # Deflection Check
        if self.fb_deflection <= self.max_deflection:
            print(
                colored(
                    f"Deflection Check - OK, Stress Ratio: {self.fb_deflection / self.max_deflection}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam Fatigue Check", "red"))

        # Key Dimensions
        self.track_distribution_width = (
            self.global_defs.tie_design_width + self.min_ballast_below_tie
        )  # AREMA 1.3.4.2.2.b
        self.track_dist_length = (
            3 * units("ft") + self.min_ballast_below_tie
        )  # AREMA 1.3.4.2.2.a

        # Dead Loads
        self.flooring_load = self.floor_load_on_fbs
        self.track_load = self.track_assembly_load_on_deck_plate

        # Live Load
        self.longitudinal_dist = self.track_dist_length
        self.lateral_dist = self.track_distribution_width

        self.dist_axel_load = self.load_values.axel_load / (
            self.longitudinal_dist * self.lateral_dist
        )

        # Impact Load # AREMA 15.1.3.5
        self.L = self.floorbeam_spacing
        self.deck_pl_impact_L = (40 - (3 * self.L**2 / (1600 * units("ft^2")))) * 0.9

        self.impact_load = (self.dist_axel_load * self.deck_pl_impact_L / 100).to(
            "lbf/ft^2"
        )

        # Rocking Effect
        self.rocking_effect = self.load_values.rocking_percent * self.dist_axel_load / 2

        self.deck_pl_dead_load = self.flooring_load + self.track_load
        self.deck_pl_live_load_impact_re = (
            self.dist_axel_load + self.impact_load + self.rocking_effect
        )

        self.total_dist_load = self.deck_pl_dead_load + self.deck_pl_live_load_impact_re

        # Compute Forces and Stresses over a 1' unit width
        self.flange_width = min(self.end_floorbeam.flange_width, self.fb.flange_width)

        self.flange_width.to("ft")

        self.M1_w = (
            1
            / 12
            * (
                (3 * self.floorbeam_spacing * self.flange_width / 2)
                - (self.floorbeam_spacing**2)
                - (3 * self.flange_width**2 / 8)
            )
        ).to("ft^2")
        self.M2_w = self.floorbeam_spacing**2 / 24

        self.gov_M_w = max(abs(self.M1_w), abs(self.M2_w))

        self.deck_pl_dl_M = self.gov_M_w * self.deck_pl_dead_load
        self.deck_pl_ll_M = self.gov_M_w * self.deck_pl_live_load_impact_re
        self.deck_pl_tot_M = self.deck_pl_dl_M + self.deck_pl_ll_M

        self.deck_pl_S_x = self.deck_plate_width * self.deck_plate_thickness**2 / 6

        # //TODO - Check Units on this one
        self.deck_pl_F_b = (
            self.deck_pl_tot_M * (12 * units("in")) / self.deck_pl_S_x
        ).to("psi")

        self.deck_pl_F_b_allow = 0.55 * self.global_defs.F_y

        # Floor Plate Stress Check
        if self.deck_pl_F_b <= self.deck_pl_F_b_allow:
            print(
                colored(
                    f"Floor Plate Stress Check - OK, Stress Ratio: {self.deck_pl_F_b / self.deck_pl_F_b_allow}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Plate Allowable Stress Check", "red"))

        # Floor Plate Deflection
        self.deck_plate_I_x = self.deck_plate_width * self.deck_plate_thickness**3 / 12
        self.deck_plate_span_L = self.floorbeam_spacing

        self.deck_pl_live_load_deflection = (
            self.deck_pl_live_load_impact_re * units("in") * self.floorbeam_spacing**4
        ) / (384 * self.global_defs.E_steel * self.deck_plate_I_x)
        self.deck_pl_allow_deflection = (self.floorbeam_spacing / 640).to("in").to("in")

        self.deck_pl_live_load_deflection = self.deck_pl_live_load_deflection.to("in")

        # Deflection Check
        if self.deck_pl_live_load_deflection <= self.deck_pl_allow_deflection:
            print(
                colored(
                    f"Deck Plate Deflection Check - OK, Stress Ratio: {self.deck_pl_live_load_deflection / self.deck_pl_allow_deflection}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Plate Deflection Check", "red"))

        # Floor Beams
        # end_bearing_stiff_width = (end_floorbeam.flange_width - end_floorbeam.web_thickness) / 2 * 4 / 4
        self.end_bearing_stiff_width = 5.75 * units("in")

        # Geometrics
        self.end_fb_spacing = 2.6 * units(
            "ft"
        )  # //TODO - References VOID fb - non-bracing sheet
        self.flooring_on_girder = (
            self.end_fb_spacing / 2 + (self.floor_length - self.span_length) / 2
        )
        # railroad_gage  # //TODO - Defined twice in excel

        # Dead Load
        # Diaphragms
        self.diaphragm.weight = 61 * units(
            "lbf/ft"
        )  # //TODO - Doesn't match section: W16x89
        self.diaphragm_quantity = 1  # //TODO - Why is this only 1 in excel?

        self.diaphragm_length = self.floorbeam_spacing / 2

        self.lateral_bracing_length = 8.20 * units(
            "ft"
        )  # //TODO - why is this redefined and lower

        self.diaphragm_P = (
            self.diaphragm.weight * self.diaphragm_quantity * self.diaphragm_length
        )

        self.end_floorbeam_dl_V = (self.end_floorbeam.weight * self.girder_spacing) / 2
        self.end_floorbeam_dl_M = self.end_floorbeam.weight * self.girder_spacing**2 / 8

        self.end_diaphragm_dl_V = self.diaphragm_P / 2
        self.end_diaphragm_dl_M = (
            self.diaphragm_P * self.end_bearing_stiff_width / 4
        )  # //TODO - Verify End stiff width

        # //TODO - Verify no bracing on end floorbeams
        # bracing_P = lateral_bracing.weight * bracing_quant * lateral_bracing_length
        # end_lateral_bracing_V = bracing_P / 2
        # end_lateral_bracing_M = bracing_P * girder_spacing / 4

        # Floor assembly between stop plates
        self.end_floor_assembly_V = (
            self.ballast_plates_clear_space
            * self.floor_load_on_fbs
            * self.flooring_on_girder
            / 2
        )
        # //TODO - Verify Flooring on girder, not fb spacing

        self.end_floor_assembly_M = (
            (
                self.floor_load_on_fbs
                * self.flooring_on_girder
                * self.ballast_plates_clear_space
            )
            / 4
            * (self.girder_spacing - self.ballast_plates_clear_space / 2)
        )

        # Floor assembly over stop plates
        self.end_fb_applied_width = (
            self.girder_spacing - self.ballast_plates_clear_space
        ) / 2

        self.end_floor_over_stop_pl_V = (
            self.floor_load_over_stop_plates
            * self.end_fb_applied_width
            * self.flooring_on_girder
        )
        self.end_floor_over_stop_pl_M = (
            self.floor_load_over_stop_plates
            * self.end_fb_applied_width**2
            / 2
            * self.flooring_on_girder
        )

        # Track assembly weight
        self.end_track_area_load_V = (
            self.track_area_load_on_fbs
            * self.ballast_plates_clear_space
            / 2
            * self.flooring_on_girder
        )
        self.end_track_area_load_M = (
            self.track_area_load_on_fbs
            * self.ballast_plates_clear_space
            / 4
            * (self.girder_spacing - self.ballast_plates_clear_space / 2)
            * self.flooring_on_girder
        )

        self.total_end_fb_dl_shear = sum(
            [
                self.end_floorbeam_dl_V,
                self.end_diaphragm_dl_V,
                self.end_floor_assembly_V,
                self.end_floor_over_stop_pl_V,
                self.end_track_area_load_V,
            ]
        )

        self.total_end_fb_dl_moment = sum(
            [
                self.end_floorbeam_dl_M,
                self.end_diaphragm_dl_M,
                self.end_floor_assembly_M,
                self.end_floor_over_stop_pl_M,
                self.end_track_area_load_M,
            ]
        )

        # Live Load
        # AREMA 15-1.3.4.2.3 Alternative live load axel
        self.end_fb_P_ll = 1.15 * self.fb.A * self.floorbeam_spacing / self.fb.s
        self.end_fb_P_2_ll = self.fb_P_ll / 2

        self.end_fb_A = self.fb.a
        self.end_fb_D = self.floorbeam_spacing
        self.end_fb_S = self.fb.s
        self.end_fb_a = self.fb.a

        self.end_fb_M_ll = self.end_fb_P_ll * self.end_fb_a / 2

        # Impact Live Load
        self.end_fb_impact_ll_percent = (
            40 - 3 * self.girder_spacing.magnitude**2 / 1600
        ) / 100

        self.end_fb_P_imp_ll = (
            self.end_fb_impact_ll_percent
            * self.end_fb_P_2_ll
            * self.load_values.ballasted_deck_reduction
        )

        self.end_fb_M_imp = self.fb_P_imp_ll * self.fb.a

        # Rocking Load  AREMA 1.3.5.d
        self.end_R1_rocking = (
            self.end_fb_P_2_ll
            * self.load_values.rocking_percent
            * (1 - 2 * self.a / self.girder_spacing)
        )

        self.end_fb_M_re = self.R1_rocking * self.a

        # Wind Force on Loaded Bridge
        self.wind_load = 300 * units("lbf/ft")
        self.end_fb_pws = (
            self.wind_load
            * self.load_values.wind_load_h
            * self.floorbeam_spacing
            / self.global_defs.railroad_gage
        )

        self.end_fb_wind_R1 = self.end_fb_pws * (1 - 2 * self.a / self.girder_spacing)

        self.end_fb_M_wl = self.end_fb_wind_R1 * self.fb.a

        # Required Section Properties and gov moment  # AREMA Table 15-1-11
        self.end_fb_M_tot_1 = sum(
            [
                self.total_end_fb_dl_moment,
                self.end_fb_M_ll,
                self.end_fb_M_imp,
                self.end_fb_M_re,
            ]
        )
        self.end_fb_M_tot_2 = (
            sum(
                [
                    self.total_end_fb_dl_moment,
                    self.end_fb_M_ll,
                    self.end_fb_M_imp,
                    self.end_fb_M_re,
                    self.end_fb_M_wl,
                ]
            )
            / 1.25
        )
        self.end_fb_M_tot = max(self.end_fb_M_tot_1, self.fb_M_tot_2)

        # Governing shear # //TODO - Ensure this isn't need in other calc
        self.end_fb_V_tot_1 = sum(
            [
                self.total_end_fb_dl_shear,
                self.end_fb_P_2_ll,
                self.end_fb_P_imp_ll,
                self.end_R1_rocking,
            ]
        )
        self.end_fb_V_tot_2 = (
            sum(
                [
                    self.total_end_fb_dl_shear,
                    self.end_fb_P_2_ll,
                    self.end_fb_P_imp_ll,
                    self.end_R1_rocking,
                    self.end_fb_wind_R1,
                ]
            )
            / 1.25
        )
        self.end_fb_V_tot = max(self.end_fb_V_tot_1, self.end_fb_V_tot_2)

        self.dead_load_per_jack = self.total_dead_load / 4

        # Shear and moment doubled to meet requirements of 11-1.8.1
        self.jacking_V_tot = self.dead_load_per_jack * 2
        self.jacking_M_tot = (
            2 * self.dead_load_per_jack * self.load_values.jack_pt_offset
        )

        # Required Section Properties
        self.end_fb_gov_M = max(self.jacking_M_tot, self.end_fb_M_tot)
        self.end_fb_gov_V = max(self.jacking_V_tot, self.end_fb_V_tot)

        self.end_fb_S_x_req = (self.end_fb_gov_M / (0.55 * self.global_defs.F_y)).to(
            "in^3"
        )

        # Holes - Assume 4 x 1" holes in web for diaphragm
        self.D1 = 3 * units("in")  # //TODO - is this a constant?
        self.D2 = 3 * units("in") + self.D1

        self.I_holes_web = (
            self.diaphragm_num_holes
            / 2
            * (self.diaphragm_dia_hole * self.end_floorbeam.web_thickness)
            * self.D1**2
        ) + (
            self.diaphragm_num_holes
            / 2
            * (self.diaphragm_dia_hole * self.end_floorbeam.web_thickness)
            * self.D2**2
        )

        self.I_holes_flange = (
            self.lateral_num_holes
            * self.lateral_dia_holes
            * self.fb.flange_thickness
            * (self.fb.depth / 2 - self.fb.flange_thickness / 2) ** 2
        )

        self.I_net = self.fb.I_x - self.I_holes_web - self.I_holes_flange

        self.S_x_net = self.I_net / (self.fb.depth / 2)

        # Allowable Stress (AREMA Table 15-1-12)
        self.Fb_ten = 0.55 * self.global_defs.F_y

        # Compression in extreme fiber
        self.Fb_comp_1 = (
            0.55 * self.global_defs.F_y
            - (
                0.55
                * self.global_defs.F_y**2
                / (6.3 * math.pi**2 * self.global_defs.E_steel)
            )
            * (self.max_diaphragm_spacing / self.fb.r_y) ** 2
        )
        self.Fb_comp_2 = (
            0.131
            * math.pi
            * self.global_defs.E_steel
            / (
                self.max_diaphragm_spacing
                * self.fb.depth
                * (1 + self.global_defs.poisson_ratio) ** 0.5
                / (self.fb.flange_thickness * self.fb.flange_width)
            )
        ).to("psi")
        self.Fb_comp_3 = 0.55 * self.global_defs.F_y

        self.F_b_comp = (min(self.Fb_comp_3, max(self.Fb_comp_1, self.Fb_comp_2))).to(
            "ksi"
        )

        self.f_b_act = (self.fb_M_tot / self.S_x_net).to("ksi")

        # Bearing area allowable stress
        if self.f_b_act < self.F_b_comp:
            print(
                colored(
                    f"Bearing Area Allowable Stress Check - OK, Stress Ratio: {self.f_b_act / self.F_b_comp}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam Allowable Stress Check", "red"))

        # End Shear
        self.R_dl = self.total_fb_dl_shear
        self.R_ll = self.fb_P_ll
        self.R_imp = self.fb_P_imp_ll * 2
        self.R_re = self.R1_rocking
        self.R_wl = self.fb_wind_R1

        self.R_tot = sum([self.R_dl, self.R_ll, self.R_imp, self.R_re, self.R_wl])

        # Assume 6x1" dia holes in web to connect to girder
        self.fs_net = (
            self.R_tot
            / (
                (
                    self.fb.depth
                    - self.web_conn_girder_holes_num * self.web_conn_girder_holes_dia
                )
                * self.fb.web_thickness
            )
        ).to("ksi")

        self.F_v = (0.35 * self.global_defs.F_y).to("ksi")

        # Bearing area allowable stress
        if self.fs_net < self.F_v:
            print(
                colored(
                    f"Bearing Area Allowable Stress - OK, Stress Ratio: {self.fs_net / self.F_v}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam End Shear Check", "red"))

        # Bolted Connection - Checked in sep. calc, they account for combined effect so no 1.25 increase
        # AREMA 15 1.5.9.a.1 # //TODO - Investigate this standard

        # Floor beam fatigue
        self.fb_fat_imp_M = self.assumed_mean_impact_perc * self.fb_M_imp
        self.fb_M_fat = self.fb_M_ll + self.fb_fat_imp_M

        self.fb_live_load_stress_range = (self.fb_M_fat / self.S_x_net).to("ksi")

        # N >= 2,000,000 Category B Table 15-1-10 Detail 2.2
        self.fb_fsr = 16 * units("ksi")

        # Floor Beam Fatigue Check
        if self.fb_live_load_stress_range < self.fb_fsr:
            print(
                colored(
                    f"Floor Beam Fatigue Check - OK, Stress Ratio: {self.fb_live_load_stress_range / self.fb_fsr}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam Fatigue Check", "red"))

        # Deflection
        self.fb_defl_M = self.fb_M_ll + self.fb_M_imp + self.fb_M_re

        self.fb_w = 8 * self.fb_defl_M / (self.girder_spacing**2)

        self.fb_deflection = (
            (5 * self.fb_w * self.girder_spacing**4)
            / (384 * self.global_defs.E_steel * self.fb.I_x)
        ).to("in")
        self.max_deflection = (self.girder_spacing / 640).to("in")

        # Deflection Check
        if self.fb_deflection <= self.max_deflection:
            print(
                colored(
                    f"Floor Beam Deflection Check - OK, Stress Ratio: {self.fb_deflection / self.max_deflection}",
                    "green",
                )
            )
        else:
            print(colored("No Good - Floor Beam Deflection Check", "red"))


if __name__ == "__main__":
    test_bridge = TPG()
