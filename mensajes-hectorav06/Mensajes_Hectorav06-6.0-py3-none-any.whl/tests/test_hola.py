import unittest
import numpy as np
from paquete.hola.saludos import generar_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0, 1, 2, 3, 4, 5]),
            generar_array(6)
        )



from paquete.hola.saludos import *
from paquete.adios.despedidas import *

saludar()
Saludo()

despedir()
Despedida()