# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
   name='biodivmap',        # 项目名
   version='0.0.7',       # 版本号
   description='Biodiversity mapping',
   packages=find_packages(),   # 包括在安装包内的Python包
   author='Zijie Wang',
   install_requires=[
        'numpy',
        'geopandas',
    ],
)