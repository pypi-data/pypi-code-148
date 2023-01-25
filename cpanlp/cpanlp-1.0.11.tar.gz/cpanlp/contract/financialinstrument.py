from cpanlp.contract.contract import *
class FinancialInstrument(Contract):
    def __init__(self,parties, consideration, value):
        super().__init__(parties, consideration)
        self.value = value
