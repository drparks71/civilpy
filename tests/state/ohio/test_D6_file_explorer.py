import unittest
from civilpy.state.ohio.D6_file_explorer import test_init


class TestD6FileExplorer(unittest.TestCase):
    def test_file_explorer_init(self):
        self.assertEqual(test_init, True)


if __name__ == '__main__':
    unittest.main()
