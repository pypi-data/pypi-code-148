from cpanlp.account.income.revenue import *
from cpanlp.entity.LLC import *
from cpanlp.market.commodity import *
import math

class Market:
    def __init__(self,commodity,participants):
        self.commodity = commodity
        self.participants = participants
        self.transaction_costs = None
        self.free_entry=None
        self.number_of_participants = None 
class PerfectlyCompetitiveMarket(Market):
    def __init__(self, commodity, participants):
        #price takers
        super().__init__(commodity, participants)
        self.equilibrium_price = None
        self.equilibrium_quantity = None
        self.barriers = False
        self.free_entry = True
        self.number_of_participants = math.inf
    def calculate_equilibrium(self):
        # Code to calculate equilibrium price and quantity
        pass
class MonopolyMarket(Market):
    def __init__(self, commodity, businessentity):
        super().__init__(commodity, [])
        self.businessentity=businessentity
        self.profit_maximizing_price = None
        self.profit_maximizing_quantity = None
        self.market_demand = None
        self.total_cost = None
        self.barriers = True
        self.free_entry = False
class OligopolyMarket(Market):
    def __init__(self, commodity, participants):
        super().__init__(commodity, participants)
        self.barriers = True
        self.free_entry = False

    def price_setting(self):
        """Price setting behavior of firms in oligopoly market"""
        for firm in self.participants:
            if firm.market_leader:
                # Firm sets price based on competitors' reactions
                pass
            else:
                # Firm sets price based on market leader's price
                pass
            
def main():
    commodity=Commodity("苹果",5,30,10,20)
    llc=LLC("tech","game",2000)
    llc1=LLC("sina","entertain",3000)
    a= Market(commodity,[llc,llc1])
    print(a.commodity.demand)
if __name__ == '__main__':
    main()