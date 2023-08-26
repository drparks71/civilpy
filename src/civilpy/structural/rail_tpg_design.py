from civilpy.structural.steel import W, MC
from civilpy.general import units


class GlobalDefinitions:
    def __init__(
            self,
            f_y=50000 * units('psi'),
            f_u=65000 * units('psi'),
            e_steel=29000000 * units('psi'),
            tie_length=8.5 * units('ft'),
            tie_width=8 * units('inch'),
            tie_depth=7 * units('inch'),
            tie_design_width=8 * units('ft'),  # Design width for distributed loading, length
            max_tie_spacing=24 * units('inch'),  # used for dead load
            future_ballast=12 * units('inch'),
            future_ballast_quantity=1,
            tie_material='Concrete',
            tie_spacing=1.5 * units('ft'),
            railroad_gage=4 * units('ft') + 8.5 * units('inch'),  # //TODO - Verify: Not AREMA
            poisson_ratio=0.30,
            steel_unit_weight=490 * units('lbf/ft^3'),
            ballast_unit_weight=120 * units('lbf/ft^3'),
            tie_unit_weight=150 * units('lbf/ft^3'),
            track_unit_weight=200 * units('lbf/ft'),
            waterproofing_unit_weight=2 * units('lbf/ft^2'),
            steel_connection_contingency=.1,
            asphalt_unit_weight=150 * units('lbf/ft^3'),
            timber_unit_weight=60 * units('lbf/ft^3'),
    ):
        super().__init__()
        self.F_y = f_y
        self.F_u = f_u
        self.E_steel = e_steel
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
    def __init__(self, diaphragm_weight_ft=61 * units('lbf/ft'),
                 diaphragm_quant=1, bracing_quant=4, fb_a=100 * units('kip'), fb_s=5 * units('ft'),
                 ballasted_deck_reduction=.9, rocking_percent=.2, wind_load=300 * units('lbf/ft'),
                 wind_load_h=8 * units('ft'), axel_load=100 * units('kips'), reduction_fact=.9,
                 wheel_load_percentage=.2,
                 # //TODO - Replace these values with a simpler table lookup
                 e80_50_ft=1901.80 * units('kip*ft'),
                 e80_55_ft=2233.10 * units('kip*ft'),
                 end_diaphragm_weight_per_ft=61 * units('lbf/ft'),
                 end_diaphragm_quantity=1,
                 axel_alternative_live_load=100 * units('kips'),
                 jack_pt_offset=3.75 * units('ft')
                 ):
        self.diaphragm_weight_ft = diaphragm_weight_ft
        self.diaphragm_quant = diaphragm_quant
        self.bracing_quant = bracing_quant
        self.fb_a = fb_a
        self.fb_s = fb_s
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


class TPG(GlobalDefinitions, LoadDefinitions):
    def __init__(
            self,
            floorbeam_spacing=2.6 * units('ft'),
            floorbeam_quantity=19,
            end_floorbeam_quantity=2,

            # FB Definitions
            # //TODO - Replace the following values with rolled beam values if we usually use rolled beams
            fb_bracket_flange_t=0.75 * units('inch'),
            fb_bracket_flange_web=8.0 * units('inch'),
            fb_bracket_flange_len=3.33 * units('foot'),
            fb_bracket_web_t=.5 * units('inch'),
            fb_bracket_web_width=1.83 * units('ft'),
            fb_bracket_web_height=2.75 * units('ft'),
            fb_bracket_quantity=12,

            # Girder Definitions
            girder_spacing=20 * units('ft'),
            girder_web_height=60 * units.inch,
            girder_web_thickness=0.625 * units.inch,
            girder_flange_width=20 * units.inch,
            girder_flange_thickness=1.625 * units.inch,

            # Diaphragm Definitions
            max_diaphragm_spacing=10.00 * units('ft'),
            diaphragm_quantity=20,

            # Hole Definitions
            diaphragm_dia_hole=1.0 * units('in'),
            diaphragm_num_holes=4,
            end_diaphragm_hole_quantity=6,

            lateral_dia_holes=1.0 * units('in'),
            lateral_num_holes=2,
            web_conn_girder_holes_num=6,
            web_conn_girder_holes_dia=1 * units('in'),

            span_length=52.00 * units('ft'),
            girder_length=54 * units('ft'),
            floor_length=58 * units('ft'),
            floor_quantity=1,
            rail_quantity=1,
            asphaltic_plank_t=1 * units('in'),
            ballast_plate_spacing=3 * units('ft'),
            asphaltic_plank_quant=1,

            # Deck plate definitions
            deck_plate_thickness=0.75 * units('in'),
            min_ballast_below_tie=6 * units('in'),
            deck_plate_width=12.00 * units('in'),

            waterproofing_quant=1,
            ballast_under_ties_t=9 * units('in'),
            ballast_under_ties_quant=1,
            tie_level_ballast_quant=1,
            tie_level_ballast_sloped_reduction=2 * units('ft^2'),
            tie_level_ballast_include_pre_move_weight=False,
            # //TODO - Verify what these diagonal/horizontal formulas/values are dependent on
            dia_stop_pl_t=.5 * units('in'),
            dia_stop_pl_width=((1 * units('ft') + 10 * units('inch')) ** 2 + (
                    1 * units.ft + (1 + 3 / 16) * units('inch')) ** 2) ** .5,
            dia_stop_pl_quantity=40,
            horizontal_upper_floor_pl_t=0.50 * units('in'),
            horizontal_upper_floor_pl_width=((1 + 10 / 12 + 13 / 16 / 12) + 3 / 12) * units('ft'),
            horizontal_upper_floor_pl_quantity=10,
            girder_quantity=2,
            assumed_mean_impact_perc=.35,  # AREMA Table 15-1-8

            # Bracing Values
            bracing_section='MC10x33.6',
            lateral_bracing_length=32.8024 * units('ft'),
            lateral_bracing_quantity=4,

            # Stiffener Values
            trans_stiff_da=96 * units('inch'),
            trans_stiff_actual_da=60 * units.inch,
            stiffener_width_bst=6 * units('in'),
            stiffener_thickness_tst=0.5 * units('in'),
            bearing_stiffener_thickness_tsb=1 * units('in'),
            bearing_stiffener_corner_clip=1 * units('in'),
            bearing_stiffener_fillet_weld_leg=0.3125 * units('in'),

            floorbeam=W('W24x250'),
            end_floorbeam=W('W21X166'),
            diaphragm=W('W16X89'),
            lateral_bracing=MC('MC10x33.6'),

            # Loads Load Definitions
            load_values=LoadDefinitions(),

            # Loads Global Variables (Non-bridge specific)
            global_values=GlobalDefinitions(),

    ):
        GlobalDefinitions.__init__(self, f_y=global_values.F_y, f_u=global_values.F_u,
                                   e_steel=global_values.E_steel,
                                   tie_length=global_values.tie_length,
                                   tie_width=global_values.tie_width,
                                   tie_depth=global_values.tie_depth,
                                   tie_design_width=global_values.tie_design_width,
                                   max_tie_spacing=global_values.max_tie_spacing,
                                   tie_material=global_values.tie_material,
                                   tie_spacing=global_values.tie_spacing,
                                   future_ballast=global_values.future_ballast,
                                   future_ballast_quantity=global_values.future_ballast_quantity,
                                   railroad_gage=global_values.railroad_gage,
                                   poisson_ratio=global_values.poisson_ratio,
                                   steel_unit_weight=global_values.steel_unit_weight,
                                   ballast_unit_weight=global_values.ballast_unit_weight,
                                   tie_unit_weight=global_values.tie_unit_weight,
                                   track_unit_weight=global_values.track_unit_weight,
                                   waterproofing_unit_weight=global_values.waterproofing_unit_weight,
                                   steel_connection_contingency=global_values.steel_connection_contingency,
                                   asphalt_unit_weight=global_values.asphalt_unit_weight,
                                   timber_unit_weight=global_values.timber_unit_weight
                                   )

        LoadDefinitions.__init__(self,
                                 diaphragm_weight_ft=load_values.diaphragm_weight_ft,
                                 diaphragm_quant=load_values.diaphragm_quant,
                                 bracing_quant=load_values.bracing_quant,
                                 fb_a=load_values.fb_a,
                                 fb_s=load_values.fb_s,
                                 ballasted_deck_reduction=load_values.ballasted_deck_reduction,
                                 rocking_percent=load_values.rocking_percent,
                                 wind_load=load_values.wind_load,
                                 wind_load_h=load_values.wind_load_h,
                                 axel_load=load_values.axel_load,
                                 reduction_fact=load_values.reduction_fact,
                                 wheel_load_percentage=load_values.wheel_load_percentage,
                                 # //TODO - Replace these values with a simpler table lookup
                                 e80_50_ft=load_values.e80_50_ft,
                                 e80_55_ft=load_values.e80_55_ft,
                                 end_diaphragm_weight_per_ft=load_values.end_diaphragm_weight_per_ft,
                                 end_diaphragm_quantity=load_values.end_diaphragm_quantity,
                                 axel_alternative_live_load=load_values.axel_alternative_live_load,
                                 jack_pt_offset=load_values.jack_pt_offset
                                 )

        # Global Input
        self.floorbeam_spacing = floorbeam_spacing
        self.floorbeam_quantity = floorbeam_quantity
        self.end_floorbeam_quantity = end_floorbeam_quantity

        # Steel Section inputs
        self.floorbeam = floorbeam
        self.end_floorbeam = end_floorbeam
        self.diaphragm = diaphragm
        self.lateral_bracing = lateral_bracing

        # Floorbeam Values
        # //TODO - update to read from AISC for rolled shapes
        self.fb_bracket_quantity = fb_bracket_quantity
        self.fb_bracket_flange_t = fb_bracket_flange_t
        self.fb_bracket_flange_web = fb_bracket_flange_web
        self.fb_bracket_flange_len = fb_bracket_flange_len
        self.fb_bracket_web_t = fb_bracket_web_t
        self.fb_bracket_web_width = fb_bracket_web_width
        self.fb_bracket_web_height = fb_bracket_web_height

        # Girder Geometrics
        self.girder_spacing = girder_spacing
        self.girder_web_height = girder_web_height
        self.girder_web_thickness = girder_web_thickness
        self.girder_flange_width = girder_flange_width
        self.girder_flange_thickness = girder_flange_thickness
        self.fb_a = self.girder_spacing / 2 - self.railroad_gage / 2

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
        self.tie_level_ballast_include_pre_move_weight = tie_level_ballast_include_pre_move_weight
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
        self.stop_plate_detail_width = (girder_spacing - self.ballast_plates_clear_space) / 2

        if self.span_length > 30 * units('ft'):
            self.impact_factor = .35  # AREMA 15 - Table 15-1-8 # //TODO - Copy
        else:
            pass

        self.L_brace = 4 * self.floorbeam_spacing
        # AREMA 15- 1.7.7.a
        self.bearing_stiffener_width_bsb = ((self.girder_flange_width - self.girder_web_thickness) / 2)

        # Basic girder geometrics definitions
        self.girder_top_flange_area = self.girder_flange_width * self.girder_flange_thickness
        self.girder_web_area = self.girder_web_height * self.girder_web_thickness
        self.girder_bot_flange_area = self.girder_flange_width * self.girder_flange_thickness

        self.girder_top_flange_centroid_height = (self.girder_flange_thickness + self.girder_web_height +
                                                  self.girder_flange_thickness / 2)
        self.girder_web_centroid_height = self.girder_flange_thickness + self.girder_web_height / 2
        self.girder_bot_flange_centroid_height = self.girder_flange_thickness / 2

        # Moment of Inertia values
        self.girder_top_flange_I_o = (self.girder_flange_width * self.girder_flange_thickness ** 3) / 12
        self.girder_web_I_o = (self.girder_web_thickness * self.girder_web_height ** 3) / 12
        self.girder_bot_flange_I_o = (self.girder_flange_width * self.girder_flange_thickness ** 3) / 12

        # Table Values depend on the following two definitions
        self.girder_height = self.girder_flange_thickness + self.girder_web_height + self.girder_flange_thickness
        self.girder_centroid = self.girder_height / 2

        # Ay^2 Values in table
        self.girder_top_flange_A_y_sq = self.girder_top_flange_area * (
                    self.girder_top_flange_centroid_height - self.girder_centroid) ** 2
        self.girder_web_A_y_sq = self.girder_web_area * (self.girder_web_centroid_height - self.girder_centroid) ** 2
        self.girder_bot_flange_A_y_sq = self.girder_top_flange_area * (
                    self.girder_bot_flange_centroid_height - self.girder_centroid) ** 2

        # Out-of-Plane I_o
        self.girder_top_flange_oop_I_o = (self.girder_flange_thickness * self.girder_flange_width ** 3) / 12
        self.girder_web_oop_I_o = self.girder_web_height * self.girder_web_thickness ** 3 / 12
        self.girder_bot_flange_oop_I_o = (self.girder_flange_thickness * self.girder_flange_width ** 3) / 12

        # Remaining Girder Section Properties
        self.girder_area = self.girder_top_flange_area + self.girder_web_area + self.girder_bot_flange_area
        self.girder_I_xx = (self.girder_top_flange_I_o + self.girder_web_I_o + self.girder_bot_flange_I_o +
                            self.girder_top_flange_A_y_sq + self.girder_web_A_y_sq + self.girder_bot_flange_A_y_sq)
        self.girder_S_xx = self.girder_I_xx / self.girder_centroid
        self.girder_r_xx = (self.girder_I_xx / self.girder_area) ** .5
        self.girder_I_yy = self.girder_top_flange_oop_I_o + self.girder_web_oop_I_o + self.girder_bot_flange_oop_I_o
        self.girder_S_yy = self.girder_I_yy / (self.girder_flange_width / 2)
        self.girder_r_yy = (self.girder_I_yy / self.girder_area) ** .5
        self.girder_weight_per_ft_no_cont = (self.girder_area * self.steel_unit_weight).to('lbf/ft')

        # No Holes
        self.girder_S_x_net = self.girder_S_xx

        #                                    # Dead Load Calculations
        # Girder
        self.girder_weight_per_ft = (self.girder_weight_per_ft_no_cont *
                                     (1 + self.steel_connection_contingency)).to('kip/ft')
        self.girder_self_load = (
                    self.girder_area * self.girder_length * self.steel_unit_weight * self.girder_quantity * (
                        1 + self.steel_connection_contingency)).to('kip')

        # Intermediate Floorbeams
        self.int_floorbeam_weight = (
                    self.girder_spacing *
                    self.floorbeam.weight *
                    self.floorbeam_quantity * (1 + self.steel_connection_contingency)).to('kips')

        # End Floor Beams
        self.end_floorbeam_weight = (
                    self.girder_spacing * self.end_floorbeam.weight *
                    self.end_floorbeam_quantity * (1 + self.steel_connection_contingency)).to('kips')

        self.total_floorbeam_weight = self.end_floorbeam_weight + self.int_floorbeam_weight

        # Diaphragms
        self.total_diaphragm_weight = (
                    self.floorbeam_spacing *
                    self.diaphragm.weight *
                    self.diaphragm_quantity * (1 + self.steel_connection_contingency)).to('kips')

        # Lateral Bracing # //TODO - lateral bracing quantity seems low
        self.total_lateral_weight = (self.lateral_bracing_length *
                                     self.lateral_bracing.weight *
                                     self.lateral_bracing_quantity * (1 + self.steel_connection_contingency)).to('kips')

        # Floor
        self.deck_plate_lin_weight_per_girder = (self.deck_plate_thickness *
                                                 self.ballast_plates_clear_space * self.steel_unit_weight * (
                                                         1 + self.steel_connection_contingency) / 2).to('lbf/ft')
        self.floor_area_load = (self.deck_plate_thickness *
                                self.steel_unit_weight * (1 + self.steel_connection_contingency)).to('lbf/ft^2')

        self.total_floor_weight = (
                    self.deck_plate_thickness *
                    self.ballast_plates_clear_space *
                    self.floor_length *
                    self.steel_unit_weight * self.floor_quantity * (1 + self.steel_connection_contingency)).to('kip')

        # Diagonal Stop Plate # //TODO - ask about what this detail is
        self.dia_stop_pl_lin_w_per_girder = (self.dia_stop_pl_t * self.dia_stop_pl_width * self.steel_unit_weight * (
                    1 + self.steel_connection_contingency)).to('lbf/ft')
        self.dia_stop_pl_area_load = (self.dia_stop_pl_t * self.dia_stop_pl_width * self.steel_unit_weight * (
                    1 + self.steel_connection_contingency) / self.stop_plate_detail_width).to('lbf/ft^2')

        self.dia_stop_pl_weight = (
                    self.dia_stop_pl_t * self.dia_stop_pl_width * self.floorbeam_spacing * self.steel_unit_weight *
                    self.dia_stop_pl_quantity * (1 + self.steel_connection_contingency)).to('kip')

        # Horizontal Upper Floor Plate # //TODO - Ask about what this detail is
        self.horizontal_upper_fl_pl_length = 4 * self.floorbeam_spacing - 8 * units('in')  # //TODO - is this always 8"
        # //TODO - formula given says (1+C), which is hard coded as 10.4, figure out what this is,
        # //TODO - also width has bad math in excel
        self.horizontal_upper_fl_pl_weight_per_girder = (self.horizontal_upper_floor_pl_t *
                                                         self.horizontal_upper_floor_pl_width *
                                                         self.steel_unit_weight *
                                                         (1 + self.steel_connection_contingency) *
                                                         self.horizontal_upper_fl_pl_length /
                                                         (10.4 * units('ft'))).to('lbf/ft')
        self.horizontal_upper_fl_pl_area_load = (self.horizontal_upper_floor_pl_t *
                                                 self.horizontal_upper_floor_pl_width *
                                                 self.steel_unit_weight * (1 + self.steel_connection_contingency) /
                                                 self.stop_plate_detail_width * self.horizontal_upper_fl_pl_length /
                                                 (10.4 * units('ft'))).to('lbf/ft^2')

        self.horizontal_upper_fl_pl_weight = (
                    self.horizontal_upper_floor_pl_t *
                    self.horizontal_upper_floor_pl_width *
                    self.horizontal_upper_fl_pl_length *
                    self.steel_unit_weight * self.horizontal_upper_floor_pl_quantity * (
                        1 + self.steel_connection_contingency)).to('kip')

        
