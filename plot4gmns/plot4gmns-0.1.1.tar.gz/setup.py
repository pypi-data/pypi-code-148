# -*- coding: utf-8 -*-
# @Time    : 2022/12/20 14:56
# @Author  : Praise
# @File    : setup.py
# obj:

# python setup.py sdist
# python setup.py bdist
# twine upload dist/*
import setuptools
setuptools.setup(
    name='plot4gmns',
    version='0.1.1',
    author='Dr.Junhua Chen, Zanyang Cui, Xiangyong Luo',
    author_email='cjh@bjtu.edu.cn, zanyangcui@outlook.com, luoxiangyong01@gmail.com',
    url='https://github.com/PariseC/plot4gmns',
    description='An open-source academic research tool for visualizing multimodal networks for transportation system modeling and optimization',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    packages=['plot4gmns'],
    python_requires=">=3.6.0",
    install_requires=['pandas', 'shapely','numpy','seaborn','matplotlib','scipy','chardet','keplergl'],
    classifiers=['License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python :: 3']
)
