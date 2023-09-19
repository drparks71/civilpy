import unittest
from civilpy.transportation import test_transporation


class TestEnvironmentalModule(unittest.TestCase):
    def test_init(self):
        self.assertEqual(test_transporation, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
