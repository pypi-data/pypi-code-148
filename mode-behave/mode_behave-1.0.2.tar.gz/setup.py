# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:43:38 2020

@author: j.reul
"""

from setuptools import setup

setup(name='mode_behave',
      version='1.0.2',
      description='Estimation and simulation of discrete choice models',
      author='Julian Reul',
      author_email='j.reul@fz-juelich.de',
      url='https://github.com/julianreul/mode_behave',
      license='MIT',
      packages=['mode_behave_public'],
      package_dir={
          'imgs': 'imgs',
          'tests': 'tests',
          'Deployments': 'mode_behave_public/Deployments',
          'InputData': 'mode_behave_public/InputData',
          'ModelParam': 'mode_behave_public/ModelParam',
          'Visualizations': 'mode_behave_public/Visualizations',
                   },
      include_package_data=True,
      zip_safe=False)