from cpanlp.account.assets.asset import *
class InvestmentProperty(Asset):
    accounts = []
    def __init__(self, account, debit, date,tenant,address,income):
        super().__init__(account, debit, date)
        self.address = address
        self.income = income
        self.tenant = tenant
        InvestmentProperty.accounts.append(self)

        