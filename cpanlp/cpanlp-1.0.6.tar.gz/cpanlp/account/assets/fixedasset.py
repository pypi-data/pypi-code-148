from cpanlp.account.assets.asset import *
#The most important attribute of a fixed asset is its ability to generate revenue or savings for the company. This can be through the asset's use in the production of goods or services, or through cost savings from the asset's use. Other important attributes of fixed assets include durability, reliability, and maintainability, as well as the asset's ability to retain its value over time. Additionally, factors such as the asset's useful life, as well as the company's ability to effectively utilize the asset, are also important to consider when evaluating a fixed asset.
class FixedAsset(Asset):
    def __init__(self, account,debit,date,purchase_price, taxes, transportation_costs, installation_costs, professional_services_costs,life_span,location):
        super().__init__(account, debit, date)
        self.purchase_price = purchase_price
        self.taxes = taxes
        self.transportation_costs = transportation_costs
        self.installation_costs = installation_costs
        self.professional_services_costs = professional_services_costs
        self.debit=self.purchase_price + self.taxes + self.transportation_costs + self.installation_costs + self.professional_services_costs
        self.location = location
        if life_span < 1:
            raise ValueError("Value must be between 0 and 1")
        self.life_span = life_span
        self.depreciation_history = []
        self.age = 0.0
        self.is_leased=False
        self.maintainability=True
        self.cost_savings = None
    def __str__(self):
        return f"{self.account} ({self.debit}), Location: {self.location}"
    def depreciate(self, rate):
        if rate < 0 or rate > 1:
            raise ValueError("Value must be between 0 and 1")
        if self.age < self.life_span:
            self.depreciation_history.append(rate*self.debit)
            self.debit -= rate*self.debit
            self.age += 1
        else:
            print("Asset already reach its life span,no more depreciation.")
class Land(Asset):
    def __init__(self,account, debit, date,area,market_value):
        super().__init__(account, debit, date)
        self.area=area
        self.market_value=market_value
    def zoning(self):
        # method to check zoning of land
        pass
    def rental_income(self, rental_rate):
        return self.area * rental_rate
    def appreciation(self):
        return self.market_value - self.debit
    def encumbrances(self):
        # method to check if the land has any encumbrances like mortgages, liens, etc
        pass
class RealState(FixedAsset):
    pass
def main():
    a=FixedAsset("zhang",100,"2022-02-21",22,12,12,12,12,12,"beijing")
    print(a.debit)
    print(a.location)
    print(a.likely_economic_benefit)
    a.depreciate(0.33)
    a.depreciate(0.33)
    a.depreciate(0.33)
    print(a.depreciation_history)
    print(a.debit)
if __name__ == '__main__':
    main()