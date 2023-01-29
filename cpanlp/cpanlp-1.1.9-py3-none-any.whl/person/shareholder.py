from cpanlp.person.investor import *

class Shareholder(Investor):
    def __init__(self,name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference)
        self.shares = shares
    def vote_on_operating_policy(self):
            # shareholder voting on operating policy
        pass
    def vote_on_investment_plan(self):
        # shareholder voting on investment plan
        pass
    def vote_on_board_members(self):
        # shareholder voting on board members
        pass
    def vote_on_compensation(self):
        # shareholder voting on compensation for board members
        pass
    def vote_on_financial_reports(self):
        # shareholder voting on financial reports
        pass
    def vote_on_profit_distribution(self):
        # shareholder voting on profit distribution
        pass
    def vote_on_capital_increase_or_decrease(self):
        # shareholder voting on capital increase or decrease
        pass
    def vote_on_bond_issuance(self):
        # shareholder voting on bond issuance
        pass
    def vote_on_merger_dissolution(self):
        # shareholder voting on merger, dissolution or change of company form
        pass
    def vote_on_amending_articles_of_incorporation(self):
        # shareholder voting on amending articles of incorporation
        pass
class MajorShareholder(Shareholder):
    def __init__(self, name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares, voting_power):
        super().__init__(name, age, wealth,utility_function,portfolio, expected_return, risk_preference,shares)
        self.voting_power = voting_power
        self.shares = shares