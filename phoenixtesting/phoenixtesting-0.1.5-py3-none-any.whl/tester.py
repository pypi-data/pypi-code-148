class Test():
    """Testing Calculator"""
    def test_addition(self):
        """Testing Addition"""
        self.assertEquals(self.test_obj.addition(1,2),3)

    def test_subtraction(self):
        """Testing Subtraction"""
        self.assertEquals(self.test_obj.subtraction(1,2),-1)

    def test_multiplication(self):
        """Testing Multiplication"""
        self.assertEquals(self.test_obj.multiplication(1,2),2)


