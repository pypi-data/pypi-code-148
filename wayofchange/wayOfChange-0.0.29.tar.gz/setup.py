#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='wayOfChange',
      version='0.0.29',
      description='Put description here',
      author='Edrihan Levesque',
      author_email='Edrihan@gmail.com',
      url='https://github.com/wayofchange',
      packages=find_packages(exclude=['test']),
      py_modules = ['wayOfChange'],

      #install_requires=['numpy',],#Put this in pyproject.toml
      #data_files={
      #  "wayOfChange": ["*.ttf"],
      #  "wayOfChange": ["fonts/*.ttf"],
      #              },'''
      package_data={'wayOfChange': ['*.ttf']},
     )