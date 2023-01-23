from cpanlp.account.assets.asset import *
from cpanlp.cas import Cas
#The most important attribute of inventory is its ability to meet customer demand and support the operations of a business. This includes the inventory's availability, reliability, and quality. Other important attributes of inventory include its cost, turnover rate, and level of obsolescence. Additionally, factors such as the inventory's ability to be easily tracked and managed, as well as the company's ability to effectively forecast and plan for inventory needs, are also important to consider when evaluating inventory.
class Inventory(Asset):
    def __init__(self, account, debit, date,net_realizable_value):
        super().__init__(account, debit, date)
        self.net_realizable_value = net_realizable_value
        self.impairment_loss =  max(0, self.debit - self.net_realizable_value)
        self.CAS= Cas.INVENTORY
        self.quality= None
        self.turnover_rate = None
        self.level_of_obsolescence = None
        self.is_confirmed = (self.likely_economic_benefit and self.is_measurable)
        self.definiton = "存货是指企业在日常活动中持有以备出售的产成品或商品、处在生产过程中的在产品、在生产过程或提供劳务过程中耗用的材料和物料等。"
    def value(self):
        return min(self.debit, self.net_realizable_value)
def main():
    a= Inventory("原材料",20,"2022-01-01",2000)
    b=a.definiton
    print(b)
    print(a.is_confirmed)
    c=a.value()
    print(c)
if __name__ == '__main__':
    main()