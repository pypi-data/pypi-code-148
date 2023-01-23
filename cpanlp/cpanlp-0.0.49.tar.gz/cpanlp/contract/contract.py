from datetime import datetime
from datetime import timedelta
#In accounting, the most important attribute of a contract is its ability to be accurately recorded and reported. This is important because contracts often have a significant impact on a company's financial performance and the accurate recording of contract terms and obligations is essential for the preparation of financial statements. Other important attributes of contracts include their completeness, validity, and enforceability. Additionally, factors such as the ability to recognize revenue or liabilities at the appropriate time, in compliance with accounting standards, and the ability to track and report contract terms and performance are also important to consider when evaluating contracts in accounting.
class Contract:
    def __init__(self, parties, consideration):
        self.contract_number = None
        self.parties = parties
        self.consideration = consideration
        self.offer = None
        self.acceptance = None
        self.legality = None
        self.start_date = None
        self.end_date = None
        self.transaction_cost=None
        self.is_active = True
        self.hidden_terms = False
        self.is_complete = True
        self.enforceability = True
        self.clauses=[]
    def default(self):
        """Function to handle a default in a contract"""
        print(f'{self.parties} has been defaulted')
    # Additional code to handle the default, such as sending a notice or taking legal action
class LoanContract(Contract):
    #The basic agreement in a labor contract is: B will do what A asks him to do for the term of the contract, in return for a given salary.
    def __init__(self, parties,  consideration, interest_rate):
        super().__init__(parties, consideration)
        self.interest_rate = interest_rate
        self.repayment_terms =None
        self.collateral = None
        self.prepayment = None
        self.amortization_schedule = []
        self.insurance = None
    def calculate_amortization(self):
        remaining_balance = self.consideration
        current_date = datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.strptime(self.end_date, '%Y-%m-%d')
        interest = self.calculate_interest_payment(self.start_date)
        while current_date <= end_date:
            principal = self.consideration * self.interest_rate / (1 - (1 + self.interest_rate) ** -(end_date - current_date).days)
            remaining_balance -= principal
            self.amortization_schedule.append({"date": current_date, "interest": interest, "principal": principal, "remaining_balance": remaining_balance})
            current_date += timedelta(days=30)
    def calculate_interest_payment(self, date):
        end_date = datetime.strptime(self.end_date, "%Y-%m-%d").date()
        start_date = datetime.strptime(date, "%Y-%m-%d").date()
        interest = (self.consideration * self.interest_rate * (end_date -start_date).days) / 365
        return interest
    def calculate_principal_payment(self, date):
        principal = 0
        for payment in self.amortization_schedule:
            if payment["date"] == date:
                principal = payment["principal"]
                break
        return principal
class LaborContract(Contract):
    def __init__(self, parties, consideration,salary):
        super().__init__(parties, consideration)
        self.employee = None
        self.employer = None
        self.salary = salary

def main():
    print(11)
if __name__ == '__main__':
    main()