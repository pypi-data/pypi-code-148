from cpanlp.contract.financialinstrument import *
from cpanlp.account.assets.asset import *

class FinancialAsset(Asset,FinancialInstrument):
    def __init__(self, account, debit,date,parties, consideration, value):
        Asset.__init__(self, account, debit,date)
        FinancialInstrument.__init__(self,parties, consideration, value)

