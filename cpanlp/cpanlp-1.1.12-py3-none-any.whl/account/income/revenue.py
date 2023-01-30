import numpy as np
from cpanlp.account.assets.financialasset.accountsreceivables import *
from cpanlp.control.control import *
from cpanlp.market.goods import *
# In accounting, the most important attribute of a sale is its ability to be recorded accurately and in a timely manner. This is important because sales are the primary source of revenue for a business and the accurate recording of sales transactions is essential for the preparation of financial statements. Other important attributes of sales include their completeness, validity, and accuracy. Additionally, factors such as the recognition of revenue at the appropriate time, compliance with accounting standards, and the ability to track and report sales by product or customer are also important to consider when evaluating sales in accounting.
class Sale(Goods):
    accounts = []
    def __init__(self, customer,goods, fair_value,market_price, supply, demand, quantity, unit_price,date):
        super().__init__(goods, fair_value,market_price, supply, demand)
        self.customer=customer
        self.quantity = quantity
        self.unit_price = unit_price
        self.date=date
        self.supply_curve = {1:3,1:4}
        self.demand_curve = {1:3,1:4}
        self.accuracy= None
        self.completeness = None
        self.validity = None
        Sale.accounts.append(self)
        
# Revenue 指的是公司在一定时期内从销售商品或提供服务中获得的收入。它是在销售过程中产生的收入，不包括其它来源的收入。Income 指的是公司在一定时期内所有来源的收入总和。除了销售收入，还包括其它来源的收入，如投资收益、利息收入、租金收入等。revenue 是 income 的一部分，但是 income 不一定包括 revenue。简单来说，Revenue 是指销售收入，而 Income 是指

class Revenue(Sale):
    accounts = []
    def __init__(self, credit,customer,goods, fair_value,market_price, supply, demand, quantity, unit_price,date):
        super().__init__(customer,goods, fair_value,market_price, supply, demand, quantity, unit_price,date)
        self.credit=credit
        self.revenue_list =[3,2]
        self.revenue_list = np.array(self.revenue_list)
        self.mean = np.mean(self.revenue_list)
        self.median = np.median(self.revenue_list)
        self.var = np.var(self.revenue_list)
        self.total= sum(self.revenue_list)
        self.goods_control=None
        self.confirm = "确认收入" if self.goods_control is None else "不能确认收入"
        self.non_cash_consideration =""
        self.financing_terms  =""
        Revenue.accounts.append(self)
    #销售合同中存在的重大融资成分
    def __str__(self):
        return f"Income(income_list={self.revenue_list}, customer={self.customer}, date={self.date})"
    def recognize_revenue(self,product_info: dict = {'current_payment_obligation': True,'ownership_transferred': False,'physical_transfer': False,'risk_and_reward_transferred': False,'accepted_by_customer': False,'other_indicators_of_control': False}): 
         #确认销售收入
 # 企业就该商品享有现时收款权利，即客户就该商品负有现时付款义务
        if product_info['current_payment_obligation']:
            return True# 企业已将该商品的法定所有权转移给客户，即客户已拥有该商品的法定所有权
        elif product_info['ownership_transferred']:
            return True# 企业已将该商品实物转移给客户，即客户已实物占有该商品
        elif product_info['physical_transfer']:
            return True# 企业已将该商品所有权上的主要风险和报酬转移给客户，即客户已取得该商品所有权上的主要风险和报酬
        elif product_info['risk_and_reward_transferred']:
            return True# 客户已接受该商品
        elif product_info['accepted_by_customer']:
            return True# 其他表明客户已取得商品控制权的迹象
        elif product_info['other_indicators_of_control']:
            return True# 其他情况均不确认销售收入
        else:
            return False
    def confirm_revenue(self,amount):
        self.credit += amount
    def evaluate_contract(self,contract):
        """评估合同，并返回各单项履约义务的类型
    """
        # 创建字典，用于存储各单项履约义务的类型
        milestones_type = {}
        # 遍历合同中的单项履约义务
        for milestone_name, milestone in contract.items():
            # 确定履约义务的类型
            if milestone[1] == 'time-based':
                milestones_type[milestone_name] = 'time-based'
            else:
                milestones_type[milestone_name] = 'point-in-time'
        # 返回字典
        return milestones_type
    def generate_receivable(self,consideration,due_date):
        b = AccountsReceivable(self.goods, [self.quantity * self.unit_price],self.date,self.customer,consideration,[self.quantity * self.unit_price],due_date)
        return b
class RevenueRule:
    def __init__(self, name, role):
        self.name = name
        self.role = role
    def is_principal(self):
        return self.role == "Principal"
    def is_agent(self):
        return self.role == "Agent"
class NonOperatingIncome:
    def __init__(self, income_type="投资所得", amount=100):
         self.income_type = income_type
         self.amount = amount
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class RevenueChecker:
    def __init__(self):
        self.clf = LogisticRegression()
        self.vectorizer = TfidfVectorizer()
        
    def fit(self, X, y):
        X_vectors = self.vectorizer.fit_transform(X)
        self.clf.fit(X_vectors, y)
    
    def predict(self, text):
        text_vector = self.vectorizer.transform([text])
        return self.clf.predict(text_vector)

# Example usage
def main():
    sale1=Sale("zhang","apple",29,300,100,100,100,29,"2022-01-01")
    hin=Revenue(2900,"zhang","apple",29,300,100,100,100,29,"2022-01-01")
    print(hin.customer)
    X = ["I made a sale of $25000", "I closed a deal worth $35000", "I sold a product for $40000", "I earned $60000 from commissions", "I made $75000 in sales","you are beautiful","it is sunny,today"]
    y = [0, 1, 1, 1, 1,0,0]
    checker = RevenueChecker()
    checker.fit(X, y)
    print(checker.predict("it is cool,today")) # [0]
    print(checker.predict("I closed a deal for $50000")) # [1]
if __name__ == '__main__':
    main()