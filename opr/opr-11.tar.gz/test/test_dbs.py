# This file is placed in the Public Domain.


"database"


import unittest


from opr.objects import Db


class TestDbs(unittest.TestCase):

    def test_constructor(self):
        dbs = Db()
        self.assertEqual(type(dbs), Db)
