import unittest
from civilpy.structural.steel import SteelSection, WBeam, hello_world
import pint

units = pint.UnitRegistry()


def test_helloworld_no_params():
    assert hello_world() == "Hello World!"


def test_hello_world_with_param():
    assert hello_world("Everyone") == "Hello Everyone!"


class TestSteelMemberFunctions(unittest.TestCase):
    def test_general_import(self):
        test_beam = SteelSection("W44X335")  # Correct Name
        test_beam2 = SteelSection("W44x335")  # Lowercase correction
        test_beam3 = SteelSection("W 44x335")  # Space in label

        self.assertEqual(test_beam.weight, test_beam2.weight)  # Verify all three names are imported identically
        self.assertEqual(test_beam2.weight, test_beam3.weight)

    def test_general_attributes(self):
        test_beam = SteelSection("W44X335")
        self.assertEqual(test_beam.weight, 335.0)
        self.assertEqual(test_beam.area, 98.5)
        self.assertEqual(test_beam.special_note, 'F')
        self.assertEqual(test_beam.I_x, 31100.0)
        self.assertEqual(test_beam.Z_x, 1620.0)
        self.assertEqual(test_beam.S_x, 1410.0)
        self.assertEqual(test_beam.r_x, 17.8)
        self.assertEqual(test_beam.I_y, 1200.0)
        self.assertEqual(test_beam.Z_y, 236.0)
        self.assertEqual(test_beam.S_y, 150.0)
        self.assertEqual(test_beam.r_y, 3.49)

    def test_WBeam_import(self):
        t = WBeam("W36X150")
        self.assertEqual(t.depth, 35.9 * units.inch)
        self.assertEqual(t.detailing_depth, 35.875 * units.inch)
        self.assertEqual(t.flange_width, 12.0 * units.inch)
        self.assertEqual(t.detailing_flange_width, 12.0 * units.inch)
        self.assertEqual(t.web_thickness, 0.625)
        self.assertEqual(t.detailing_web_thickness, 0.625)
        self.assertEqual(t.half_web_detail, 0.3125)
        self.assertEqual(t.flange_thickness, 0.94)
        self.assertEqual(t.detailing_flange_thickness, 0.9375)
        self.assertEqual(t.k_design, 1.69)
        self.assertEqual(t.k_detailing, 2.1875)
        self.assertEqual(t.k1, 1.5)
        self.assertEqual(t.slenderness_ratio_flange, 6.37)
        self.assertEqual(t.slenderness_ratio_web, 51.9)
        self.assertEqual(t.J, 10.1)
        self.assertEqual(t.Cw, 82200.0)
        self.assertEqual(t.Wno, 105.0)
        self.assertEqual(t.Sw1, 294.0)
        self.assertEqual(t.Qf, 93.1)
        self.assertEqual(t.Qw, 287.0)
        self.assertEqual(t.radius_of_gyration, 3.06)
        self.assertEqual(t.flange_centroid_distance, 35.0)
        self.assertEqual(t.exposed_perimeter, 105.0)
        self.assertEqual(t.shape_perimeter, 117.0)
        self.assertEqual(t.box_perimeter, 83.8)
        self.assertEqual(t.exposed_box_perimeter, 95.8)
        self.assertEqual(t.web_face_depth, 31.5)
        self.assertEqual(t.fastener_workable_gage, 5.5)


if __name__ == '__main__':
    unittest.main()
