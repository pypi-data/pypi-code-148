"""
# -*- coding: utf-8 -*-
__author__ = "CodeWithLaksh"
__email__ = "dashlakshyaraj2006@gmail.com"
__version__ = 1.0.0"
__copyright__ = "Copyright (c) 2004-2020 Leonard Richardson"
# Use of this source code is governed by the MIT license.
__license__ = "MIT"
Description:
            calculator_cwl is a package that does the basic math calculation.
            This is a simple oops and match-case based calculator made using python.
Documentation:
            Github: https://github.com/codewithlaksh/calculator_cwl
            PyPi: https://pypi.org/user/laksh2552/
"""
__version__ = 1.0
## Warning: This code is valid for only Python 3.10.xx and later because the match-case is newly introduced in python 3.10.
class Calculator:
    def add(self):
        return self.a + self.b

    def subtract(self):
        return self.a - self.b

    def multiply(self):
        return self.a * self.b

    def divide(self):
        return self.a / self.b

while True:
    calc = Calculator()
    a = float(input("Enter your first number: "))
    b = float(input("Enter your second number: "))
    calc.a = a
    calc.b = b
    choices = [1, 2, 3, 4]
    print('''
    Guidelines:
    1. Enter 1 for addition
    2. Enter 2 for subtraction
    3. Enter 3 for multiplication
    4. Enter 4 for division
    ''')
    choice = int(input("Enter your choice (1 or 2 or 3 or 4): "))
    if choice not in choices:
        print("Please enter a valid choice!")
        choice = int(input("Enter your choice (1 or 2 or 3 or 4): "))
    else:
        match choice:
            case 1:
                print("Sum of the two numbers is", calc.add())
            case 2:
                print("Difference of the two numbers is", calc.subtract())
            case 3:
                print("Product of the two numbers is", calc.multiply())
            case 4:
                print("Remainder after division of the two numbers is", calc.divide())
        wantsToContinue = input("Do you wish to continue ? (y for yes, n for no): ")
        wantsToContinue_choices = ["y", "n"]
        if (wantsToContinue not in wantsToContinue_choices):
            wantsToContinue = input("Please enter \"y for yes, n for no\": ")
        else:
            if (wantsToContinue == "y"):
                continue
            elif (wantsToContinue == "n"):
                print("Thanks for using our calculator!")
                break