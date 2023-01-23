from datetime import datetime
class Acquisition:
    def __init__(self, target_company, acquiring_company, price):
        self.target_company = target_company
        self.acquiring_company = acquiring_company
        self.price = price
        self.leverage_ratio = None
        self.date = datetime.now()
class HostileAcquisition(Acquisition):
    def __init__(self, target_company, acquiring_company, price, hostile_tactic):
        super().__init__(target_company, acquiring_company, price)
        self.hostile_tactic = hostile_tactic

def main():
    print(666)
if __name__ == '__main__':
    main()