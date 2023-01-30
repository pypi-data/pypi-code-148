from cpanlp.stakeholder.stakeholder import *

class Public(Stakeholder):
    def __init__(self, name,type,capital, interests,power):
        super().__init__(name,type,capital, interests,power)
        self.voice=""