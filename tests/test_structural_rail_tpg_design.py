from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from src.civilpy.structural.rail_tpg_design import TPG


class TestTPG(TestCase):
    t = TPG()

    def test_run_calcs(self):
        self.assertLessEqual(self.t.fb_deflection, self.t.max_deflection)