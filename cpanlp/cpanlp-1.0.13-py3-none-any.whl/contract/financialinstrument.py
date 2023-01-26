from cpanlp.contract.contract import *
class FinancialInstrument(Contract):
    def __init__(self,parties, consideration,obligations, value):
        super().__init__(parties, consideration,obligations)
        self.value = value
