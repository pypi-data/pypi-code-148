from cpanlp.contract.contract import *
class LaborContract(Contract):
    accounts = []
    def __init__(self, parties, consideration,obligations,salary):
        super().__init__(parties, consideration,obligations)
        self.employee = None
        self.employer = None
        self.salary = salary
        LaborContract.accounts.append(self)