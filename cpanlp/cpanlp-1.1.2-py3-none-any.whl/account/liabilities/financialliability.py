from cpanlp.contract.financialinstrument import *
from cpanlp.account.liabilities.liability import *
class FinancialLiability(Liability,FinancialInstrument):
    accounts = []
    def __init__(self, account, credit, due_date,rate,parties, consideration, value):
        Liability.__init__(self, account, credit, due_date,rate)
        FinancialInstrument.__init__(self,parties, consideration, value)
        FinancialLiability.accounts.append(self)

