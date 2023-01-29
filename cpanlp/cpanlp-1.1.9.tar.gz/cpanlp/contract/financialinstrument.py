from cpanlp.contract.contract import *
class FinancialInstrument(Contract):
    accounts = []
    def __init__(self,parties, consideration,obligations, value):
        super().__init__(parties, consideration,obligations)
        self.value = value
        FinancialInstrument.accounts.append(self)
