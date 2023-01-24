import sys
sys.path.append(sys.path[0] + '/../toolkit-gm')
from eta import Eta

import unittest
from unittest.mock import patch

from time import sleep


@patch('builtins.print')


class TestETA(unittest.TestCase):


    def test_eta(self, mock_print):
        eta = Eta()

        # Begin logs 
        eta.begin(2, 'Hello World')
        mock_print.assert_called_with('Hello World - Elapsed: [00h00\'00] - ETA [??h??\'??] -   0.00%')

        # Iter logs
        sleep(1.1)
        eta.iter()
        mock_print.assert_called_with('\x1b[1A\x1b[KHello World - Elapsed: [00h00\'01] - ETA [00h00\'01] -  50.00%')

        # End logs
        eta.iter()
        eta.end()
        mock_print.assert_called_with('\x1b[1A\x1b[KHello World is done - Elapsed: [00h00\'01]')







if __name__ == '__main__': unittest.main()