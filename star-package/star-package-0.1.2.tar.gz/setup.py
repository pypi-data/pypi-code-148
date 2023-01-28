#! /usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='star-package',  # 包的名字
    author='liu yang',  # 作者
    version='0.1.2',  # 版本号
    license='MIT',

    description='some tools',
    long_description='''some tools''',

    author_email='otakzliu@163.com',
    packages=setuptools.find_packages(),

    # 依赖包
    install_requires=[
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)


