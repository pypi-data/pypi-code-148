"""
### -*- coding: utf-8 -*-
__author__ = "CodeWithLaksh"
__email__ = "dashlakshyaraj2006@gmail.com"
__version__ = 1.0.0"
__copyright__ = "Copyright (c) 2004-2020 Leonard Richardson"
### Use of this source code is governed by the MIT license.
__license__ = "MIT"
Description:
            calculator_cwl is a package that does the basic math calculation.
            This is a simple oops and match-case based calculator made using python.
Documentation:
            Github: https://github.com/codewithlaksh/calculator_cwl
            PyPi: https://pypi.org/user/laksh2552/
"""
__version__ = 1.2
import argparse
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="calculator_cwl"+str(__version__))
    parser.parse_args()

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

sys.exit(main())