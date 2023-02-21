import unittest

# Import dicts to make sure they still exist
from civilpy.state.ohio.dot import help_function, basemap_labels, bridge_labels, drainage_labels, geotechnical_labels
from civilpy.state.ohio.dot import landscaping_labels, lighting_labels, mot_labels, row_labels, roadway_labels
from civilpy.state.ohio.dot import signal_labels, traffic_control_labels, utility_labels, wall_labels, all_labels
from civilpy.state.ohio.dot import ohio_counties, NBIS_state_codes, state_code_conversion, get_3_digit_st_cd_from_2

# Import functions to test them
from civilpy.state.ohio.dot import get_bridge_data_from_tims


class TestDotFunctions(unittest.TestCase):
    def test_help_function(self):
        self.assertEqual(help_function(), None)

    def test_dicts(self):
        self.assertEqual(basemap_labels['KB'], '3D Model KB')
        self.assertEqual(bridge_labels['SB'], 'Bearing')
        self.assertEqual(drainage_labels['XD'], 'Channel Cross Sections')
        self.assertEqual(geotechnical_labels['YL'], 'Geohazard Boring Logs')
        self.assertEqual(landscaping_labels['PD'], 'Details')
        self.assertEqual(lighting_labels['LC'], 'Circuit Diagrams')
        self.assertEqual(mot_labels['XM'], 'Cross Sections')
        self.assertEqual(row_labels['RC'], 'Centerline Plat')
        self.assertEqual(roadway_labels['GC'], 'Calculations/Computations')
        self.assertEqual(signal_labels['CD'], 'Details')
        self.assertEqual(traffic_control_labels['TC'], 'Calculations/Computations')
        self.assertEqual(utility_labels['UC'], 'Calculations/Computations')
        self.assertEqual(wall_labels['WC'], 'Calculations/Computations')
        self.assertEqual(all_labels['basemap_labels']['KB'], '3D Model KB')
        self.assertEqual(ohio_counties['ADAMS'], 'ADA')
        self.assertEqual(NBIS_state_codes['014'], 'Alabama')

    def test_get_bridge_data_from_tims(self):
        self.assertEqual(get_bridge_data_from_tims()['SFN'], '6500609')

    def test_state_code_conversion(self):
        self.assertEqual(state_code_conversion(39), 'Ohio')

    def test_get_3_digit_st_cd_from_2(self):
        self.assertEqual(get_3_digit_st_cd_from_2(39), '395')
