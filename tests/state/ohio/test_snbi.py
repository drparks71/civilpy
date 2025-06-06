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

# import unittest
# from src.civilpy.state.ohio.snbi import SNBITransfer
# from unittest.mock import patch, PropertyMock

# Removed to stop hitting TIMs API
#
# class TestSNBITransitionObject(unittest.TestCase):
#     def setUp(self, sfn="2701464"):
#         # Creates a 'test bridge' and makes sure none of the attributes have changed
#         self.tb = SNBITransfer(sfn)
#
#     def test_snbi_transfer_results(self):
#         # Creates a 'test bridge' and makes sure none of the attributes have changed
#         self.assertEqual(self.tb.transition_record["BID01"], None)
#         self.assertEqual(self.tb.transition_record["BID02"], None)
#         self.assertEqual(self.tb.transition_record["BID03"], None)
#         self.assertEqual(self.tb.transition_record["BL01"], None)
#         self.assertEqual(self.tb.transition_record["BL02"], None)
#         self.assertEqual(self.tb.transition_record["BL03"], None)
#         self.assertEqual(self.tb.transition_record["BL04"], "BL_04_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BL05"], None)
#         self.assertEqual(self.tb.transition_record["BL06"], None)
#         self.assertEqual(self.tb.transition_record["BL07"], None)
#         self.assertEqual(self.tb.transition_record["BL08"], "BL_08_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BL09"], None)
#         self.assertEqual(self.tb.transition_record["BL10"], None)
#         self.assertEqual(self.tb.transition_record["BL11"], None)
#         self.assertEqual(self.tb.transition_record["BL12"], None)
#         self.assertEqual(self.tb.transition_record["BCL01"], "BCL_01_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BCL02"], "BCL_02_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BCL03"], "BCL_03_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BCL04"], None)
#         self.assertEqual(self.tb.transition_record["BCL05"], None)
#         self.assertEqual(self.tb.transition_record["BCL06"], None)
#         self.assertEqual(
#             self.tb.transition_record["BSP01"],
#             {"1": None, "2": None, "3": None, "4": None},
#         )
#         self.assertEqual(self.tb.transition_record["BSP02"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BSP03"], None)
#         self.assertEqual(self.tb.transition_record["BSP04"], {"1": None, "2": None})
#         self.assertEqual(
#             self.tb.transition_record["BSP05"],
#             {"1": None, "2": None, "3": None, "4": None},
#         )
#         self.assertEqual(self.tb.transition_record["BSP06"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BSP07"], None)
#         self.assertEqual(self.tb.transition_record["BSP08"], None)
#         self.assertEqual(self.tb.transition_record["BSP09"], None)
#         self.assertEqual(self.tb.transition_record["BSP10"], None)
#         self.assertEqual(self.tb.transition_record["BSP11"], None)
#         self.assertEqual(self.tb.transition_record["BSP12"], None)
#         self.assertEqual(self.tb.transition_record["BSP13"], None)
#         self.assertEqual(self.tb.transition_record["BSB01"], None)
#         self.assertEqual(self.tb.transition_record["BSB02"], None)
#         self.assertEqual(self.tb.transition_record["BSB03"], None)
#         self.assertEqual(self.tb.transition_record["BSB04"], None)
#         self.assertEqual(self.tb.transition_record["BSB05"], None)
#         self.assertEqual(self.tb.transition_record["BSB06"], None)
#         self.assertEqual(self.tb.transition_record["BSB07"], None)
#         self.assertEqual(self.tb.transition_record["BRH01"], None)
#         self.assertEqual(self.tb.transition_record["BRH02"], None)
#         self.assertEqual(self.tb.transition_record["BG01"], None)
#         self.assertEqual(self.tb.transition_record["BG02"], None)
#         self.assertEqual(self.tb.transition_record["BG03"], "B.G_03_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BG04"], None)
#         self.assertEqual(self.tb.transition_record["BG05"], None)
#         self.assertEqual(self.tb.transition_record["BG06"], None)
#         self.assertEqual(self.tb.transition_record["BG07"], None)
#         self.assertEqual(self.tb.transition_record["BG08"], None)
#         self.assertEqual(self.tb.transition_record["BG09"], None)
#         self.assertEqual(self.tb.transition_record["BG10"], "B.G_10_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BG11"], None)
#         self.assertEqual(self.tb.transition_record["BG12"], None)
#         self.assertEqual(self.tb.transition_record["BG13"], None)
#         self.assertEqual(self.tb.transition_record["BG14"], None)
#         self.assertEqual(self.tb.transition_record["BG15"], None)
#         self.assertEqual(self.tb.transition_record["BG16"], None)
#         self.assertEqual(self.tb.transition_record["BF01"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BF02"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BF03"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BRT01"], None)
#         self.assertEqual(
#             self.tb.transition_record["BRT02"],
#             {"1": "B.RT_02_CHECK_1_FAILED", "2": "B.RT_02_CHECK_2_FAILED"},
#         )
#         self.assertEqual(self.tb.transition_record["BRT03"], "B.RT_03_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BRT04"], "B.RT_04_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BRT05"], "B.RT_05_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BH01"], "B.H_01_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BH02"], "B.H_02_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BH03"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH04"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH05"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH06"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH07"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH08"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH09"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH10"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH11"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH12"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH13"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH14"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH15"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH16"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH17"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BH18"], {"1": None, "2": None})
#         self.assertEqual(self.tb.transition_record["BRR01"], None)
#         self.assertEqual(
#             self.tb.transition_record["BRR02"],
#             {"1": "B.RR_02_CHECK_1_FAILED", "2": "B.RR_02_CHECK_2_FAILED"},
#         )
#         self.assertEqual(
#             self.tb.transition_record["BRR03"],
#             {"1": "B.RR_03_CHECK_1_FAILED", "2": "B.RR_03_CHECK_2_FAILED"},
#         )
#         self.assertEqual(self.tb.transition_record["BN01"], None)
#         self.assertEqual(
#             self.tb.transition_record["BN02"],
#             {"1": "B.N_02_CHECK_1_FAILED", "2": "B.N_02_CHECK_2_FAILED", "3": None},
#         )
#         self.assertEqual(
#             self.tb.transition_record["BN03"],
#             {
#                 "1": "B.N_03_CHECK_1_FAILED",
#                 "2": "B.N_03_CHECK_2_FAILED",
#                 "3": "B.N_03_CHECK_3_FAILED",
#             },
#         )
#         self.assertEqual(self.tb.transition_record["BN04"], "B.N_04_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BN05"], None)
#         self.assertEqual(self.tb.transition_record["BN06"], "B.N_06_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BLR01"], None)
#         self.assertEqual(self.tb.transition_record["BLR02"], None)
#         self.assertEqual(self.tb.transition_record["BLR03"], None)
#         self.assertEqual(self.tb.transition_record["BLR04"], "B.LR_04_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BLR05"], "B.LR_05_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BLR06"], "B.LR_06_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BLR07"], None)
#         self.assertEqual(self.tb.transition_record["BLR08"], None)
#         self.assertEqual(self.tb.transition_record["BPS01"], None)
#         self.assertEqual(self.tb.transition_record["BPS02"], None)
#         self.assertEqual(self.tb.transition_record["BEP01"], None)
#         self.assertEqual(self.tb.transition_record["BEP02"], None)
#         self.assertEqual(self.tb.transition_record["BEP03"], None)
#         self.assertEqual(self.tb.transition_record["BEP04"], None)
#         self.assertEqual(self.tb.transition_record["BIR01"], "B.IR_01_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BIR02"], None)
#         self.assertEqual(self.tb.transition_record["BIR03"], "B.EP_03_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BIR04"], None)
#         self.assertEqual(
#             self.tb.transition_record["BIE01"],
#             {
#                 "1": "B.IE_01_CHECK_1_FAILED",
#                 "2": "B.IE_01_CHECK_2_FAILED",
#                 "3": "B.IE_01_CHECK_3_FAILED",
#                 "4": "B.IE_01_CHECK_4_FAILED",
#                 "5": "B.IE_01_CHECK_5_FAILED",
#                 "6": "B.IE_01_CHECK_6_FAILED",
#                 "7": "B.IE_01_CHECK_7_FAILED",
#             },
#         )
#         self.assertEqual(
#             self.tb.transition_record["BIE02"],
#             {
#                 "1": "B.IE_01_CHECK_1_FAILED",
#                 "2": "B.IE_01_CHECK_2_FAILED",
#                 "3": "B.IE_01_CHECK_3_FAILED",
#                 "4": "B.IE_01_CHECK_4_FAILED",
#                 "5": "B.IE_01_CHECK_5_FAILED",
#                 "6": "B.IE_01_CHECK_6_FAILED",
#                 "7": "B.IE_01_CHECK_7_FAILED",
#             },
#         )
#         self.assertEqual(self.tb.transition_record["BIE03"], None)
#         self.assertEqual(self.tb.transition_record["BIE04"], None)
#         self.assertEqual(
#             self.tb.transition_record["BIE05"],
#             {
#                 "1": None,
#                 "2": "B.IE_05_CHECK_2_FAILED",
#                 "3": "B.IE_05_CHECK_3_FAILED",
#                 "4": "B.IE_05_CHECK_4_FAILED",
#             },
#         )
#         self.assertEqual(self.tb.transition_record["BIE06"], None)
#         self.assertEqual(self.tb.transition_record["BIE07"], None)
#         self.assertEqual(self.tb.transition_record["BIE08"], None)
#         self.assertEqual(self.tb.transition_record["BIE09"], None)
#         self.assertEqual(self.tb.transition_record["BIE10"], None)
#         self.assertEqual(self.tb.transition_record["BIE11"], None)
#         self.assertEqual(self.tb.transition_record["BIE12"], None)
#         self.assertEqual(self.tb.transition_record["BC01"], None)
#         self.assertEqual(self.tb.transition_record["BC02"], None)
#         self.assertEqual(self.tb.transition_record["BC03"], None)
#         self.assertEqual(self.tb.transition_record["BC04"], None)
#         self.assertEqual(self.tb.transition_record["BC05"], None)
#         self.assertEqual(self.tb.transition_record["BC06"], None)
#         self.assertEqual(self.tb.transition_record["BC07"], None)
#         self.assertEqual(self.tb.transition_record["BC08"], None)
#         self.assertEqual(self.tb.transition_record["BC09"], None)
#         self.assertEqual(self.tb.transition_record["BC10"], None)
#         self.assertEqual(self.tb.transition_record["BC11"], None)
#         self.assertEqual(self.tb.transition_record["BC12"], "B.C_12_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BC13"], "B.C_13_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BC14"], None)
#         self.assertEqual(self.tb.transition_record["BC15"], None)
#         self.assertEqual(self.tb.transition_record["BAP01"], "B.AP_01_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BAP02"], None)
#         self.assertEqual(self.tb.transition_record["BAP03"], None)
#         self.assertEqual(self.tb.transition_record["BAP04"], None)
#         self.assertEqual(self.tb.transition_record["BAP05"], None)
#         self.assertEqual(self.tb.transition_record["BW01"], "B.W_01_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BW02"], "B.W_02_CHECK_FAILED")
#         self.assertEqual(self.tb.transition_record["BW03"], None)
#
#     def test_snbi_transfer_bid01(self):
#         self.assertEqual(SNBITransfer.bid01(self.tb, "test1", "test1"), None)
#         self.assertEqual(
#             SNBITransfer.bid01(self.tb, "test1", "test2"), "B.ID_01_CHECK_FAILED"
#         )
#
#     def test_snbi_transfer_bid02(self):
#         self.assertEqual(SNBITransfer.bid02(self.tb), None)
#
#     def test_snbi_transfer_bid03(self):
#         self.assertEqual(SNBITransfer.bid03(self.tb), None)
#
#     def test_snbi_transfer_bl01(self):
#         self.assertEqual(self.tb.bl01(), None)
#         self.assertEqual(self.tb.bl01("test1", "test1"), None)
#         self.assertEqual(self.tb.bl01("test1", "test2"), "BL_01_CHECK_FAILED")
#
#     def test_snbi_transfer_bl02(self):
#         #        self.assertEqual(self.tb.bl02('test1', 'test1'), None)
#         self.assertEqual(self.tb.bl02(), None)
#
#     def test_snbi_transfer_bl03(self):
#         #        self.assertEqual(self.tb.bl02('test1', 'test1'), None)
#         self.assertEqual(self.tb.bl02(), None)
#
#     def test_snbi_transfer_bl04(self):
#         self.assertEqual(self.tb.bl02(), None)
#         self.assertEqual(self.tb.bl02(), None)
#         self.assertEqual(self.tb.bl02(), None)
