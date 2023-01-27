# This file is placed in the Public Domain.


"model"


import unittest


from gcid import Object
from gcid.modules.mdl import oorzaak


class TestModel(unittest.TestCase):

    def test_model(self):
        self.assertEqual(type(oorzaak), Object)
