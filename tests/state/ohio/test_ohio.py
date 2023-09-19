import unittest
from civilpy.state.ohio import test_state_ohio


class OhioInitialization(unittest.TestCase):
    def test_ohio_module(self):
        self.assertEqual(test_state_ohio, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
