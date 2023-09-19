import unittest
from civilpy.state.ohio.search_tools import test_init


class TestSearchToolsModule(unittest.TestCase):
    def test_search_module(self):
        self.assertEqual(test_init, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
