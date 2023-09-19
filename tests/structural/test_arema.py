import unittest
from civilpy.structural.arema import test_arema


class TestAremaModule(unittest.TestCase):
    def test_init(self):
        self.assertEqual(test_arema, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()