import unittest
from civilpy.environmental import test_environmental


class TestEnvironmentalModule(unittest.TestCase):
    def test_init(self):
        self.assertEqual(test_environmental, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
