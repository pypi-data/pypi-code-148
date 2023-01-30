from cpanlp.stakeholder.stakeholder import *

class Government(Stakeholder):
    def __init__(self, name,type,capital, interests,power):
        super().__init__(name,type,capital, interests,power)
    def regulate_company(self, company):
        # Code to regulate the company
        pass
    def make_policy(self, policy):
        # Code to make a policy
        pass