from cpanlp.person.consumer import *

class Partner(Consumer):
    def __init__(self, name, age,wealth,utility_function,share):
        super().__init__(name, age,wealth,utility_function)
        self.share = share