# -*- coding: utf-8 -*-

from setuptools import setup

setup(
   name='scikit-geo',        # 项目名
   version='0.0.1',       # 版本号
   description='scikit geography',
   packages=['CV'],   # 包括在安装包内的Python包
   author='Zijie Wang',
   install_requires=["numpy","pandas","geopandas","rasterio","rasterstats"]
)