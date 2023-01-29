from unittest import TestCase

from compo.compo import Compo


class Component(TestCase):
    def test_pydentic_rendering_of_nested_components(self):
        assert Compo()
