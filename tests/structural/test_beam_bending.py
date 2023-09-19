import unittest
from civilpy.structural.beam_bending import PointLoadV, PointLoadH, PointTorque
from civilpy.structural.beam_bending import DistributedLoadV, DistributedLoadH
from civilpy.structural.beam_bending import Beam
import matplotlib


class TestLoadClasses(unittest.TestCase):
    def test_vertical_point_load(self):
        vert_load = PointLoadV(10, 5)
        self.assertEqual(vert_load.force, 10)
        self.assertEqual(vert_load.coord, 5)
        self.assertEqual(vert_load[0], 10)
        self.assertEqual(vert_load[1], 5)

    def test_horizontal_point_load(self):
        horizontal_load = PointLoadH(10, 5)
        self.assertEqual(horizontal_load.force, 10)
        self.assertEqual(horizontal_load.coord, 5)
        self.assertEqual(horizontal_load[0], 10)
        self.assertEqual(horizontal_load[1], 5)

    def test_vertical_dist_load(self):
        vert_load = DistributedLoadV("10*x+5", (0, 5))
        self.assertEqual(vert_load.expr, "10*x+5")
        self.assertEqual(vert_load.span, (0, 5))
        self.assertEqual(vert_load[0], '10*x+5')
        self.assertEqual(vert_load[1], (0, 5))

    def test_horizontal_dist_load(self):
        horizontal_load = DistributedLoadH("10*x+5", (0, 5))
        self.assertEqual(horizontal_load.expr, "10*x+5")
        self.assertEqual(horizontal_load.span, (0, 5))
        self.assertEqual(horizontal_load[0], '10*x+5')
        self.assertEqual(horizontal_load[1], (0, 5))

    def test_point_torque(self):
        torque_load = PointTorque(30, 4)
        self.assertEqual(torque_load.torque, 30)
        self.assertEqual(torque_load.coord, 4)
        self.assertEqual(torque_load[0], 30)
        self.assertEqual(torque_load[1], 4)


class TestBeam(unittest.TestCase):
    test_beam = Beam(span=20)

    def test_beam_attributes(self):
        self.assertEqual(self.test_beam.length, 20)
        self.assertEqual(self.test_beam.pinned_support, 2)
        self.assertEqual(self.test_beam.rolling_support, 8)

        self.test_beam.rolling_support = 20
        self.assertEqual(self.test_beam.rolling_support, 20)

    test_beam.add_loads([PointLoadV(30, 5)])

    def test_loaded_beam(self):
        self.assertEqual(type(self.test_beam.plot()), matplotlib.figure.Figure)



if __name__ == '__main__':
    unittest.main()
