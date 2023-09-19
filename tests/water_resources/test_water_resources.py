import unittest
from civilpy.water_resources import test_water_resources


class TestEnvironmentalModule(unittest.TestCase):
    def test_init(self):
        self.assertEqual(test_water_resources, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
