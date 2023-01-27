# This file is placed in the Public Domain.


"rss"


import unittest


from test.cmds import Fetcher


class TestRss(unittest.TestCase):

    def test_fetcher(self):
        fetcher = Fetcher()
        self.assertEqual(type(fetcher), Fetcher)
