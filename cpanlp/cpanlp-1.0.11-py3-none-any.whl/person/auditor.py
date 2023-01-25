from cpanlp.person.supervisor import *

class Auditor(Supervisor):
    def __init__(self, name, age,wealth,
utility_function):
        super().__init__(name, age,wealth,
utility_function)