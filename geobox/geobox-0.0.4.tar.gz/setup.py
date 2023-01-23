# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
   name='geobox',        # 项目名
   version='0.0.4',       # 版本号
   description='scikit geography',
   packages=find_packages(),   # 包括在安装包内的Python包
   author='Zijie Wang',
   install_requires=["numpy","pandas","geopandas","rasterio","rasterstats"]
)