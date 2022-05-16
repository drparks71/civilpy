"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest
from civilpy.water_resources.hydraulics import OhioCulvertDesign


class TestCulvertDesign(unittest.TestCase):
    # Establish a test culvert object
    def setUp(self):
        self.tc = OhioCulvertDesign()

    def test_load_culvert_design_object(self):
        self.assertEqual(
            self.tc.Headwall_Dimensions["A"]["10.5"]["L"], 12.75
        )  # add assertion here
