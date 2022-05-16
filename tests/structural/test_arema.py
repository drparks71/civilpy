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
import pandas as pd
from pathlib import Path
from unittest.mock import patch, MagicMock

from civilpy.general import units
from civilpy.structural.midas import analysis_results_request
from civilpy.structural.arema import CooperE80, LoadRatingMember


class TestCooperE80(unittest.TestCase):

    def test_initialization(self):
        cooper = CooperE80()
        self.assertEqual(cooper.series, 80)
        self.assertEqual(len(cooper.distances), 18)
        self.assertEqual(len(cooper.magnitudes), 18)
        self.assertEqual(cooper.distributed["distance"], 109 * units.feet)
        self.assertEqual(cooper.distributed["magnitude"], 8 * units("kip/ft"))

    def test_conversion_to_other_series(self):
        cooper = CooperE80(series=60)
        self.assertEqual(cooper.series, 60)
        expected_magnitudes = [
            30.0 * units("kip"),
            60.0 * units("kip"),
            60.0 * units("kip"),
            60.0 * units("kip"),
            60.0 * units("kip"),
            39.0 * units("kip"),
            39.0 * units("kip"),
            39.0 * units("kip"),
            39.0 * units("kip"),
            30.0 * units("kip"),
            60.0 * units("kip"),
            60.0 * units("kip"),
            60.0 * units("kip"),
            60.0 * units("kip"),
            39.0 * units("kip"),
            39.0 * units("kip"),
            39.0 * units("kip"),
            39.0 * units("kip"),
        ]
        for expected, actual in zip(expected_magnitudes, cooper.magnitudes):
            self.assertAlmostEqual(expected.magnitude, actual.magnitude)

    def test_str_representation(self):
        cooper = CooperE80()
        repr_string = repr(cooper)
        self.assertIn("0 foot: 40 kip", repr_string)
        self.assertIn("109 foot: 8.0 kip / foot", repr_string)
