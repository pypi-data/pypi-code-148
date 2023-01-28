from fxitily import Fxility
import unittest


class Test_pip_delta(unittest.TestCase):


    def test_pip_delta_positive(self):
        self.obj = Fxility()
        self.assertEqual(self.obj.pip_delta(1.1010,1.1020), -10, "Should be 20")
        

if __name__ == '__main__':
    unittest.main()