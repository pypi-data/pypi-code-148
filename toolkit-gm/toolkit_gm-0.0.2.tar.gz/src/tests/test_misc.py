import sys
sys.path.append(sys.path[0] + '/../toolkit-gm')
import misc

import unittest

from datetime import datetime


class TestMisc(unittest.TestCase):

    def test_percent(self):
        self.assertEqual(misc.percent(0), '  0.00%')
        self.assertEqual(misc.percent(0.0314), '  3.14%')
        self.assertEqual(misc.percent(0.1234), ' 12.34%')
        self.assertEqual(misc.percent(0.0001), '  0.01%')
        self.assertEqual(misc.percent(1.56), '156.00%')
        self.assertEqual(misc.percent(0.01), '  1.00%')
        self.assertEqual(misc.percent(-0.01), ' -1.00%')

    def test_now(self):
        self.assertEqual(misc.now(), int(datetime.now().timestamp()))




if __name__ == '__main__': unittest.main()