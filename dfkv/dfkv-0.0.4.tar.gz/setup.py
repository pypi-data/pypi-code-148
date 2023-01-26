#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
setup(
    name='dfkv',
    version='0.0.4',
    description='a expand for dict',
    long_description='expand dict, can use a.b, can set value more than 1-level a.b.c.d="xyz"',
    author='fred deng',
    author_email='dfgeoff@qq.com',
    license='Apache License 2.0',
    url='https://gitee.com/hifong45/dkv.git',
    download_url='https://gitee.com/hifong45/dkv/master.zip',
    packages=find_packages(),
    install_requires=[]
)