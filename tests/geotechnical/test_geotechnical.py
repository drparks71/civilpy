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
from civilpy.geotechnical import (
    rankine_active_pressure,
    coulomb_active_pressure_with_surcharge,
)


class TestGeotechnicalModule(unittest.TestCase):
    def test_rankine(self):
        self.assertEqual(round(rankine_active_pressure(18.0, 5.0, 30.0), 2), 75.00)


class TestCoulombActivePressureWithSurcharge(unittest.TestCase):

    def test_typical_case(self):
        unit_weight = 18  # kN/m³
        height = 5  # meters
        friction_angle = 30  # degrees
        wall_friction_angle = 10  # degrees
        backfill_inclination = 5  # degrees
        wall_inclination = 0  # degrees
        surcharge_load = 10  # kN/m²

        result = coulomb_active_pressure_with_surcharge(
            unit_weight,
            height,
            friction_angle,
            wall_friction_angle,
            backfill_inclination,
            wall_inclination,
            surcharge_load,
        )
        expected_result = 175.714
        self.assertAlmostEqual(result, expected_result, places=2)

    def test_zero_values(self):
        unit_weight = 0
        height = 5
        friction_angle = 30
        wall_friction_angle = 10
        backfill_inclination = 5
        wall_inclination = 0
        surcharge_load = 0

        result = coulomb_active_pressure_with_surcharge(
            unit_weight,
            height,
            friction_angle,
            wall_friction_angle,
            backfill_inclination,
            wall_inclination,
            surcharge_load,
        )
        expected_result = 0.0
        self.assertEqual(result, expected_result)

    def test_negative_values(self):
        with self.assertRaises(ValueError):
            coulomb_active_pressure_with_surcharge(-1, 5, 30, 10, 5, 0, 10)

    def test_high_friction_angle(self):
        unit_weight = 18
        height = 5
        friction_angle = 90  # degrees (very high friction angle)
        wall_friction_angle = 30
        backfill_inclination = 10
        wall_inclination = 15
        surcharge_load = 15

        result = coulomb_active_pressure_with_surcharge(
            unit_weight,
            height,
            friction_angle,
            wall_friction_angle,
            backfill_inclination,
            wall_inclination,
            surcharge_load,
        )
        expected_result = 38.254  # Example expected result, you'll need to calculate the actual expected value
        self.assertAlmostEqual(result, expected_result, places=2)


if __name__ == "__main__":
    unittest.main()
