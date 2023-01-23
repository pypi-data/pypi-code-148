#the most important attribute of a commodity is its ability to be accurately valued and measured. This is important because commodities are often bought and sold on a regular basis, and their value can fluctuate significantly based on market conditions. Other important attributes include the commodity's level of standardization, as well as its ease of storage and transport. Additionally, factors such as the commodity's level of substitutability and the level of competition in the market are also important to consider when evaluating a commodity in accounting.
class Commodity:
    def __init__(self, commodity, fair_value, supply, demand):
        self.name = commodity
        self.fair_value = fair_value
        self.supply = supply
        self.demand = demand
        self.supply_curve = {}
        self.demand_curve = {}
        self.level_of_standardization = None
        self.ease_of_storage = None
        self.ease_of_transport = None
        self.level_of_substitutability = None
        self.level_of_competition = None
        self.fluctuation = None
    def get_info(self):
        print(f"Name: {self.name}")
        print(f"Fair value: {self.fair_value}")
        print(f"Supply: {self.supply}")
        print(f"Demand: {self.demand}")
    def get_market_price(self):
        if self.supply > self.demand:
            print(f"The market price of {self.name} is lower than its fair value")
        elif self.supply < self.demand:
            print(f"The market price of {self.name} is higher than its fair value")
        else:
            print(f"The market price of {self.name} is equal to its fair value")
    def get_supply_demand_gap(self):
        gap = self.demand - self.supply
        if gap > 0:
            print(f"The demand for {self.name} is higher than its supply")
        elif gap < 0:
            print(f"The supply for {self.name} is higher than its demand")
        else:
            print(f"The supply and demand for {self.name} is balanced")
    def get_price_trend(self):
        if self.supply > self.demand:
            print(f"The price of {self.name} is expected to decrease in the future")
        elif self.supply < self.demand:
            print(f"The price of {self.name} is expected to increase in the future")
        else:
            print(f"The price of {self.name} is expected to remain stable in the future")
    def get_supply_curve(self):
        print(f"The supply curve for {self.name} is as follows:")
        for price, quantity in self.supply_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")   
    def get_demand_curve(self,demand_curve):
        print(f"The demand curve for {self.name} is as follows:")
        for price, quantity in demand_curve.items():
            print(f"Price: {price}, Quantity: {quantity}")
            
def main():
    print("hi")
if __name__ == '__main__':
    main()