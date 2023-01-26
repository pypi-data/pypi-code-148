#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='wayOfChange',
      #version='0.0.25',
      include_package_data=True,
      description='Put description here',
      author='Edrihan Levesque',
      author_email='Edrihan@gmail.com',
      url='https://github.com/wayofchange',
      packages=find_packages(exclude=['test']),
      install_requires=['numpy',],
      package_data={
        "wayOfChange": ["*.ttf"],
        "wayOfChange.fonts": ["*.ttf"]
                    }
     )