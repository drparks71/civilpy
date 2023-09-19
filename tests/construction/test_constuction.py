import unittest
from civilpy.construction import test_construction


class TestConstructionModule(unittest.TestCase):
    def test_init(self):
        self.assertEqual(test_construction, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
