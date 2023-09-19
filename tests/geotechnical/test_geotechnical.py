import unittest
from civilpy.geotechnical import test_geotechnical


class TestGeotechnicalModule(unittest.TestCase):
    def test_init(self):
        self.assertEqual(test_geotechnical, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
