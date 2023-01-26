from cpanlp.person.consumer import *

class Fiduciary(Consumer):
    def __init__(self, name, age,wealth, utility_function, beneficiary):
        super().__init__(name, age,wealth, utility_function)
        self.beneficiary = beneficiary