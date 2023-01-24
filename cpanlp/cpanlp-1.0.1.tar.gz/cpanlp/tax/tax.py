class Tax:
    def __init__(self, rate, base,deductions):
        self.rate = rate
        self.base = base
        self.deductions =deductions
        self.object=None
        self.payer=None
        self.incentives=None
        self.deadline=None
        self.location=None
        self.history = []
       
class TurnoverTax(Tax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)
class VAT(TurnoverTax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)
class ConsumptionTax(TurnoverTax):
    def __init__(self, rate, base,deductions):
        super().__init__(rate, base,deductions)
class IncomeTax(Tax):
    def __init__(self, rate, base, deductions):
        super().__init__(rate, base,deductions)
    def calculate(self, income):
        taxable_income = income - self.deductions
        return taxable_income * self.rate + self.base       
class PersonalIncomeTax(IncomeTax):
    def __init__(self, rate, base, deductions, exemptions):
        super().__init__(rate, base, deductions)
        self.exemptions = exemptions
class CorporateIncomeTax(IncomeTax):
    def __init__(self, rate, base, deductions, exemptions):
        super().__init__(rate, base, deductions)
        self.exemptions = exemptions
        
class PropertyTax:
    def __init__(self, rate,value):
        self.value = value
        self.rate = rate
    def calculate_tax(self):
        return self.value * self.rate
class RealEstateTax(PropertyTax):
    def __init__(self, rate,value, square_footage):
        super().__init__(rate,value)
        self.square_footage = square_footage
    def calculate_tax(self):
        base_tax = super().calculate_tax()
        return base_tax + (self.square_footage * 0.05)
class BehaviorTax:
    def __init__(self, amount):
        self.amount = amount
    def calculate_tax(self):
        return self.amount * self.rate
class TransactionTax(BehaviorTax):
    def __init__(self, amount, transaction):
        super().__init__(amount)
        self.transaction = transaction
    def calculate_tax(self):
        base_tax = super().calculate_tax()
        return base_tax + (self.transaction * 0.05)
def main():
    income = 1000
    vat = IncomeTax(0.1,200,20)
    print(vat.calculate(income))
if __name__ == '__main__':
    main()
