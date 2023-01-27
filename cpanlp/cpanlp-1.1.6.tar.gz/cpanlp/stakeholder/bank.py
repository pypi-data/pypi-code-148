from cpanlp.stakeholder.stakeholder import *

class Bank(Stakeholder):
    def __init__(self, name,type,capital, interests,power):
        super().__init__(name,type,capital, interests,power)
        self.loans = {}
    def grant_loan(self, company, amount):
        self.loans[company.name] = amount
        