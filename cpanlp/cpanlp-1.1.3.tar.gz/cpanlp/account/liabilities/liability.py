import datetime
class Liability:
    accounts = []
    def __init__(self, account, credit, due_date,rate):
        self.account = account
        self.credit = credit
        self.due_date = due_date
        self.liabilities = []
        self.asset = None
        self.rate=rate
        today = datetime.date.today()
        due_date = datetime.datetime.strptime(self.due_date, "%Y-%m-%d").date()
        if today < due_date:
            self.remaining_days = (due_date - today).days
        else:
            raise ValueError("债务已经过期，无法计算剩余天数")
        Liability.accounts.append(self)
    def make_payment(self, amount):
        self.credit -= amount
        print(f"{self.account} has made a payment of {amount}, and the remaining debt is {self.credit}.")
    def __str__(self):
        return f"Liability(account='{self.account}', amount={self.credit}, due_date='{self.due_date}')"
    def add_liability(self, rate: float, account, credit: float, due_date):
            self.liabilities.append(Liability(rate,account,credit,due_date))
    def pay_liability(self,  account, amount):
        for liability in self.liabilities:
            if liability.account == account:
                    liability.amount -= amount
                    break
    def convert_to_equity(self, value):
        self.credit -= value
    def pay_off(self):
        if self.asset is not None:
            self.credit -= self.asset.debit
            self.asset = None
        else:
            raise ValueError("No asset to use for payment.")
def main():
    print(5)
    a=Liability("zhang",100,"2025-01-01",0.2)
    print(a.remaining_days)
if __name__ == '__main__':
    main()