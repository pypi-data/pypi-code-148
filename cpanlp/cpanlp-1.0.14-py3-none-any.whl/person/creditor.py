from cpanlp.person.consumer import *

class Creditor(Consumer):
    def __init__(self, name, age, wealth,utility_function, amount):
        super().__init__(name, age, wealth,utility_function)
        self.amount = amount
