from cpanlp.entity.entity import *
from datetime import timedelta, date
import random
class LLC(IncorporatedEntity):
    def __init__(self, name,type,capital):
        super().__init__(name,type,capital)
        self.goods = []
        self.monopoly = False
        self.monopoly_start = None
        self.monopoly_end = None
        self.subsidiaries = []
        self.ownership = None
        self.control = None
        self.shareholders = []
        self.board_members = []
        self.board_of_supervisors = []
        self.independent_financial_advisor = None
        self.chairman = None
    def establish_subsidiary(self, subsidiary_name, subsidiary_type, subsidiary_capital):
        """
        Create a new subsidiary LLC 
        """
        subsidiary = LLC(subsidiary_name, subsidiary_type,subsidiary_capital)
        self.subsidiaries.append(subsidiary)
        return subsidiary
    def transfer_assets(self, subsidiary, assets):
        """
        Transfer assets to subsidiary
        """
        if subsidiary not in self.subsidiaries:
            raise ValueError(f"{subsidiary.name} is not a subsidiary of {self.name}")
        for asset in assets:
            if asset not in self.assets:
                raise ValueError(f"{asset} is not an asset of {self.name}")
            self.assets.remove(asset)
            subsidiary.assets.append(asset)
        return f"Assets {assets} are transferred to {subsidiary.name} successfully"
    def innovate(self,new_goods):
        # simulate the innovation process
        self.new_good = new_goods
        self.goods.append(new_goods)
        self.monopoly = True
        self.monopoly_start = date.today()
        # random number of years for the monopoly to last (between 1 and 5)
        monopoly_years = random.randint(1, 5)
        self.monopoly_end = self.monopoly_start + timedelta(days=365*monopoly_years)
        print(f"{self.name} has innovated and now has a temporary monopoly on {new_goods} until {self.monopoly_end}.")
    def lose_monopoly(self):
        self.monopoly = False
        self.monopoly_start = None
        self.monopoly_end = None
        print(f"{self.name}'s monopoly has ended.")
    def check_monopoly(self):
        if self.monopoly and self.monopoly_end:
            if date.today() > self.monopoly_end:
                self.lose_monopoly()
            else:
                print(f"{self.name} still has a monopoly on {self.goods[-1]} until {self.monopoly_end}.")
        else:
            print(f"{self.name} does not currently have a monopoly.")
    def imitate_product(self, company, product):
        print(f"{self.name} is imitating {product} from {company}.")
        
class AssociateCompany(LLC):
    def __init__(self, name,type,capital, parent_company):
        super().__init__(name,type,capital)
        self.parent_company = parent_company
 
class Subsidiary(LLC):
    def __init__(self, name,type,capital, parent_company):
        super().__init__(name,type,capital)
        self.parent_company = parent_company
class JointVenture(LLC):
    def __init__(self, name,type,capital, partners, project):
        super().__init__(name,type,capital)
        self.partners = partners
        self.project = project

#Joint venture 公司和 associate 公司是在商业和企业管理中常用的术语。Joint venture 公司是指两个或多个公司共同创建一个新公司，并共同拥有和管理该公司。这种公司通常是为了完成特定的项目或业务而设立的。双方公司会共同承担风险和收益。Associate 公司是指一家公司持有另一家公司的股权，但并不控制该公司的经营管理。 Associate 公司可以是一家独立的公司，也可以是一家子公司。与 Joint venture公司相比，Associate 公司的风险和收益主要由持股公司承担。总的来说，Joint venture 公司是双方公司共同创建和管理的公司，而 Associate 公司是一家公司持有另一家公司的股权，但不控制其经营管理。
def main():
    b=LLC("Partner Inc","partner",10)
    print(b.subsidiaries)
    print("hello")
if __name__ == '__main__':
    main()