from cpanlp.person.consumer import *

class Craftsman(Consumer):
    def __init__(self, name, age,wealth,utility_function,skill_level=1):
        super().__init__(name, age,wealth,utility_function)
        self.skill_level = skill_level
        self.projects = []