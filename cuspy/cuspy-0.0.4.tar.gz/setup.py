#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:56
# @Author  : zbc@mail.ustc.edu.cn
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup

with open('README.md', 'r', encoding='utf-8')as f:
    long_description = f.read()

setup(
    name='cuspy',
    version='0.0.4',
    author='zbc',
    author_email='zbc@mail.ustc.edu.cn',
    url='',
    description=u'Config Utils for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['cuspy'],
    install_requires=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5'
)


if __name__ == "__main__":
    pass
