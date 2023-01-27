# This file is placed in the Public Domain.


"scan tests"


import inspect
import unittest


from opr.handler import Command
from opr.scanner import scan

import test.cmds as cmds


class TestScan(unittest.TestCase):

    def test_scan(self):
        scan(cmds)
        self.assertTrue("cfg" in Command.cmd)
