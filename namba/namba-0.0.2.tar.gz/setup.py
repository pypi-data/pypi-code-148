# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 18:07:05 2022
@author:
Зайцева Дарья
"""

from setuptools import setup, find_packages
long_description = '''Library for the 5 semester'''
setup(name='namba',
      version='0.0.02',
      url='https://github.com/dashkazaitseva',
      packages=['namba'],
      license='MIT',
      description='',
      zip_safe=False,
      package_data={'namba': ['*.txt']},
      include_package_data=True
      )