from typing import List
#The most important attribute of equity is its ability to represent the residual ownership interest in a company after all liabilities have been paid. This means that equity represents the value of a company that is left over for shareholders after all debts have been settled. Other important attributes of equity include its growth potential, as well as its risk and return characteristics. Additionally, factors such as the level of diversification, liquidity, and the quality of the underlying assets also important to consider when evaluating equity.
class Equity:
    def __init__(self, account, value):
        self.account = account
        self.value = value
        self.equities: List[Equity] = []
        self.residual_ownership_interest=None
        self.growth_pontential=None
        self.risk_return = None
        self.diversification = None
        self.liquidity = None
        self.quality_of_underlying_assets=None
    def __str__(self):
        return f"{self.account}: {self.value}"
    def add_equity(self, account, value):
        self.equities.append(Equity(account, value))
    def withdraw_equity(self, account, value):
        for equity in self.equities:
            if equity.account == account:
                equity.value -= value
                break
    def sum(self):
        return sum([equity.value for equity in self.equities])
def main():
    a=Equity("张老板",1000)
    print(a)
    a.add_equity("liu",1000)
    print(a.equities[0])
if __name__ == '__main__':
    main()