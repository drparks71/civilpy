from io import StringIO
from unittest import TestCase
from unittest.mock import patch
from src.civilpy.structural.rail_tpg_design import TPG


class TestTPG(TestCase):

    def test_run_calcs(self):
        expected_url = """Flange Compression Check - OK
Web Thickness Check 1 - OK
Web Thickness CHeck 2 - OK
Flange Compression Check - OK
Bending Check - OK, Stress Ratio: 0.9225909060826183 force_pound / inch ** 2 / pound_force_per_square_inch
Bending Check - OK, Stress Ratio: 0.9225909060826186 dimensionless
Bending Fatigue - OK, Stress Ratio: 0.73380327114963 dimensionless
Deflection Check - OK, Ratio: 0.6307157084746534 dimensionless
Web Shear Check - OK, Stress Ratio: 0.6164890919227507 dimensionless
Weld Strength Check - OK, Stress Ratio: 0.5075830449480359 dimensionless
Transverse Stiffeners Required
Weld Strength Check - OK
Stiffener I_xx Check - OK
Stiffener Thickness Check - OK
Stiffener Weld Fatigue - OK, Stress Ratio: 0.9281306196358959 dimensionless
Longitudinal Stiffeners not required
Longitudinal Stiffeners Check - OK
Longitudinal Stiffeners Check - OK
Case 2 Controls
Bearing stiffener stress: 27155.276272613875 pound_force_per_square_inch
Longitudinal Stiffeners Check - OK, Stress Ratio: 0.5112597758960217 dimensionless
Bearing Stiffener Weld Check - OK, Stress Ratio: 0.45102357600552445 dimensionless
Bearing Area Allowable Stress Check - OK, Stress Ratio: 0.6340616578694178 dimensionless
Bearing Area Allowable Stress Check - OK, Stress Ratio: 0.3412387259725499 dimensionless
Bearing Area Allowable Stress Check - OK, Stress Ratio: 0.2502732273083372 dimensionless
Bearing Area Allowable Stress Check - OK, Stress Ratio: 0.32341725842958674 dimensionless
Deflection Check - OK, Stress Ratio: 0.24964506342823886 dimensionless
Floor Plate Stress Check - OK, Stress Ratio: 0.5755581290899663 dimensionless
Deck Plate Deflection Check - OK, Stress Ratio: 0.14099386081451015 dimensionless
Bearing Area Allowable Stress Check - OK, Stress Ratio: 0.3401055219027701 dimensionless
Bearing Area Allowable Stress - OK, Stress Ratio: 0.2502732273083372 dimensionless
Floor Beam Fatigue Check - OK, Stress Ratio: 0.32234323685584865 dimensionless
Floor Beam Deflection Check - OK, Stress Ratio: 0.24964506342823886 dimensionless
"""

        with patch('sys.stdout', new=StringIO()) as fake_out:
            TPG()
            self.assertEqual(fake_out.getvalue(), expected_url)
