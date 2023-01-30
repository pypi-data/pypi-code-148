from cpanlp.person.consumer import *
class Beneficiary(Consumer):
    def __init__(self, name, age,wealth, utility_function):
        super().__init__(name, age,wealth, utility_function)