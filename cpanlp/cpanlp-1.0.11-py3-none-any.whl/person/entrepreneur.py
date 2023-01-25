from cpanlp.person.consumer import *
from cpanlp.culture.spirit import *

class Entrepreneur(Consumer):
    def __init__(self, name, age,wealth,utility_function,experience,company,entrepreneurship):
        super().__init__(name, age,wealth,utility_function)
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
def main():
    print("hello")
        # Create an Entrepreneur
    entre = Entrepreneurship()
    john = Entrepreneur("John Smith",30,1000000,0, 5,LLC("huawei","llc",5000),entre)
if __name__ == '__main__':
    main()