import unittest
import numpy as np
from Mensajes.Bienvenidas.Saludos import generarArray

class PruebasBienvenidas(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
            generarArray(10))

