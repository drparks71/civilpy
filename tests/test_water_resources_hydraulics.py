import unittest
from civilpy.water_resources.hydraulics import CulvertDesign


class TestCulvertDesign(unittest.TestCase):
    # Establish a test culvert object
    def setUp(self):
        self.tc = CulvertDesign()

    def test_load_culvert_design_object(self):
        self.assertEqual(self.tc.Headwall_Dimensions['A']['10.5']['L'], 12.75)  # add assertion here
