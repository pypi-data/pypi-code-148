# This file is placed in the Public Domain.


"scan tests"


import unittest


from bot.handler import Command
from bot.scanner import scancmd


from bot.service import irc


class TestScan(unittest.TestCase):

    "scan unittest"

    def test_scan(self):
        "test scanning of the irc module"
        scancmd(irc)
        self.assertTrue("cfg" in Command.cmd)
