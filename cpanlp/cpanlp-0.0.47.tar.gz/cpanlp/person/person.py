from cpanlp.entity.entity import *
from cpanlp.culture.spirit import *
from cpanlp.person.utility import *
from scipy.optimize import minimize

import numpy as np
import pandas as pd
def calculate_beta(portfolio):
    # Load historical data for each stock in the portfolio
    stocks_data = {}
    for stock in portfolio:
        data = pd.read_csv(stock + ".csv")
        stocks_data[stock] = data
    # Calculate the daily returns for each stock
    returns = {}
    for stock, data in stocks_data.items():
        returns[stock] = data["Adj Close"].pct_change()
    # Calculate the covariance matrix between the returns of all stocks
    cov_matrix = np.cov(list(returns.values()))
    # Calculate the beta value of the portfolio
    beta = cov_matrix[0][1] / np.var(returns["market"])
    return beta
class Person:
    def __init__(self, name, age,wealth):
        self.name = name
        self.age = age
        self.wealth=wealth
class Consumer(Person):
    def __init__(self, name, age,wealth, utility_function):
        super().__init__(name, age,wealth)
        self.utility_function = utility_function
        self.commodity_prices=[]
        self.utility_function =utility_function
    def calculate_utility(self, goods, prices, income):
        """
        Calculates the total utility for a consumer given a set of goods, their prices, and the consumer's income
        """
        total_utility = 0
        for i in range(len(goods)):
            total_utility += self.utility_function(goods[i], prices[i], income)
        return total_utility
    def indifference_curve(self, x):
        # Indifference curve function
        # U(x1,x2) = sqrt(x1) + sqrt(x2)
        # Budget constraint: p1*x1 + p2*x2 <= income
        U=self.utility_function
        return U(x[0]) + U(x[1])
    def budget_constraint(self, x):
        p1, p2 = self.commodity_prices
        return p1 * x[0] + p2 * x[1] - self.wealth
        

class Investor(Person):
    def __init__(self,name, age, wealth,portfolio, expected_return, risk_preference):
        super().__init__(name, age,wealth)
        self.portfolio = portfolio
        self.expected_return = expected_return
        self.risk_preference = risk_preference
    def calculate_risk_neutrality(self):
        # Code to calculate the beta value of the portfolio
        beta = calculate_beta(self.portfolio)
        return beta
class Creditor(Person):
    def __init__(self, name, age, wealth, amount):
        super().__init__(name, age, wealth)
        self.amount = amount
class Shareholder(Investor):
    def __init__(self,name, age, wealth,portfolio, expected_return, risk_preference,shares):
        super().__init__(name, age, wealth,portfolio, expected_return, risk_preference)
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
    def __init__(self, name, age, wealth,portfolio, expected_return, risk_preference,shares, voting_power):
        super().__init__(name, age, wealth,portfolio, expected_return, risk_preference,shares)
        self.voting_power = voting_power
        self.shares = shares
class Craftsman(Person):
    def __init__(self, name, age,wealth,skill_level=1):
        super().__init__(name, age,wealth)
        self.skill_level = skill_level
        self.projects = []
class Employee(Person):
    def __init__(self, name, age,wealth, salary, department):
        super().__init__(name, age,wealth)
        self.emp_id = None
        self.salary = salary
        self.department = department
        self.job_title = None
        self.experience = None
        self.education = None
class Manager(Person):
    def __init__(self, name, age,wealth,title, department):
        super().__init__(name, age,wealth)
        self.title = title
        self.department = department
        self.powers = []
    def manage_production_and_operations(self):
        """Manage the company's production and operations"""
        pass
    def implement_board_resolutions(self):
        """Organize and implement the board's resolutions"""
        pass
    def implement_annual_business_plan(self):
        """Organize and implement the company's annual business plan and investment strategy"""
        pass
    def formulate_internal_management_structure(self):
        """Formulate the company's internal management structure"""
        pass
    def formulate_basic_management_system(self):
        """Formulate the company's basic management system"""
        pass
    def formulate_specific_regulations(self):
        """Formulate the company's specific regulations"""
        pass
    def propose_hiring_or_dismissal(self):
        """Propose the hiring or dismissal of the company's vice manager and financial officer"""
        pass
    def hire_or_dismiss_staff(self):
        """Decide on the hiring or dismissal of management personnel, except those that should be decided by the board"""
        pass
    def set_strategy(self, strategy):
        self.strategy = strategy
        print(f'{self.name}, {self.title} of {self.department} has set a new strategy: {strategy}')
    def make_decision(self, decision):
        print(f'{self.name}, {self.title} of {self.department} has made a decision: {decision}')
    def delegate_task(self, task, employee):
        print(f'{self.name}, {self.title} of {self.department} has delegated task: {task} to employee {employee}')
    def responsible_for_board(self):
        print("I am responsible for the board.")  
class Supervisor(Person):
    def __init__(self, name, age,wealth):
        super().__init__(name, age,wealth)
    def inspect_financials(self):
        """Inspect the company's financials"""
        pass
    def supervise_board_and_senior_management(self):
        """Supervise the actions of the board and senior management in carrying out their duties, and propose the dismissal of directors and senior management who violate laws, regulations, the company's articles of association or resolutions of the shareholders' meeting."""
        pass
    def request_corrective_action(self):
        """When the actions of the board and senior management harm the interests of the company, require them to take corrective action"""
        pass
    def propose_extraordinary_shareholders_meeting(self):
        """Propose a special shareholders' meeting, and convene and preside over the meeting when the board fails to fulfill its duty to convene and preside over shareholders' meetings"""
        pass
    def propose_resolutions(self):
        """Propose resolutions to shareholders' meeting"""
        pass
    def sue_board_and_senior_management(self):
        """Sue the board and senior management according to the provisions of Article 151 of this Law"""
        pass
    def other_responsibilities(self):
        """Other responsibilities as specified in the company's bylaws"""
        pass
class Partner(Person):
    def __init__(self, name, age,wealth,share):
        super().__init__(name, age,wealth)
        self.share = share
class Entrepreneur(Person):
    def __init__(self, name, age,wealth,experience,company,entrepreneurship):
        super().__init__(name, age,wealth)
        self.entrepreneurship=entrepreneurship
        self.experience = experience
        self.company = company
        self.industry = ""
        self.employees = []
    def hire_employee(self, employee):
        self.employees.append(employee)
        print(f"{employee.name} has been hired by {self.company.name}.")
    def fire_employee(self, employee):
        self.employees.remove(employee)
        print(f"{employee.name} has been fired by {self.company.name}.")
    def list_employees(self):
        for employee in self.employees:
            print(employee.name)
    def raise_funds(self, amount):
        print(f"{self.company.name} has raised ${amount} in funding.")
    def acquire_company(self, company):
        print(f"{self.company.name} has acquired {company.name}.")
    def take_risk(self, risk):
        if risk > self.experience:
            print(self.name + " is taking a high risk.")
        else:
            print(self.name + " is taking a moderate risk.")
    def innovate(self):
        print(self.name + " is constantly seeking new and innovative ideas.")
    def persist(self):
        print(self.name + " is persistent in the face of failure.")
    def strive_for_excellence(self):
        print(self.name + " is always striving for excellence.")
class Auditor(Person):
    def __init__(self, name, age,wealth):
        super().__init__(name, age,wealth)
def main():
    # Create an Entrepreneur
    entre = Entrepreneurship()
    john = Entrepreneur("John Smith",30,1000000, 5,LLC("huawei","llc",5000),entre)
    # Hire employees
    employee1 = Employee("zhang",19,221333,2000,"accounting")
    employee2 = Employee("zhang12",29,222233,2000,"accounting")
    john.hire_employee(employee1)
    john.hire_employee(employee2)
    # List employees
    john.list_employees()
    # Raise funds
    john.raise_funds(1000000)
    # Acquire company
    company = LLC("deloitte","auditor",20000)
    john.acquire_company(company)
    john.strive_for_excellence()
    print(john.entrepreneurship.determination)
    income = 100
    prices = [10, 20]
    U= utility(3.3)
    lucy = Consumer("lucy",23,1000,U)
    lucy.commodity_prices=prices
    x0 = [0, 0]
    constraints = {'type': 'ineq', 'fun': lucy.budget_constraint}
    res = minimize(lucy.indifference_curve, x0, constraints=constraints)
    
if __name__ == '__main__':
    main()