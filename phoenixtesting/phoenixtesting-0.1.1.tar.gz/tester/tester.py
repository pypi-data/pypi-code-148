import unittest

class Test(unittest.TestCase):

    def test_addition(self,a,b):
        self.assertEquals(self.test_obj.addition(1,2),3)

    def test_subtraction(self,a,b):
        self.assertEquals(self.test_obj.subtraction(1,2),-1)

    def test_multiplication(self,a,b):
        self.assertEquals(self.test_obj.multiplication(1,2),-1)


