import unittest
from civilpy.state.ohio.dot import SNBITransition


class TestSNBITransitionObject(unittest.TestCase):
    def setUp(self, sfn=2701464):
        # Creates a 'test bridge' and makes sure none of the attributes have changed
        self.tb = SNBITransition(sfn)

    def test_snbi_transfer_functions(self):
        # Creates a 'test bridge' and makes sure none of the attributes have changed
        self.assertEqual(self.tb.bid01(), None)
        self.assertEqual(self.tb.bid02(), None)
        self.assertEqual(self.tb.bid03(), None)
        self.assertEqual(self.tb.bl01(), None)
        self.assertEqual(self.tb.bl02(), None)
        self.assertEqual(self.tb.bl03(), None)
        self.assertEqual(self.tb.bl04(), None)
        self.assertEqual(self.tb.bl05(), None)
        self.assertEqual(self.tb.bl06(), None)
        self.assertEqual(self.tb.bl07(), None)
        self.assertEqual(self.tb.bl08(), None)
        self.assertEqual(self.tb.bl09(), None)
        self.assertEqual(self.tb.bl10(), None)
        self.assertEqual(self.tb.bl11(), None)
        self.assertEqual(self.tb.bl12(), None)
        # //TODO -  Determine correct value to get test passing
        self.assertEqual(self.tb.bcl01(), 'BCL_01_CHECK_FAILED')

