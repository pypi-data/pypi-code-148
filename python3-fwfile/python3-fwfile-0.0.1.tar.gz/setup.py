# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='python3-fwfile',
    version='0.0.1',
    author='OpusSystem',
    author_email='suporte@opussystem.com.br',
    url='https://www.opussystem.com.br',
    keywords=['fixed', 'width', 'text'],
    packages=find_packages(exclude=['*tests*']),
    include_package_data=True,
    package_data={
    },
    install_requires=[
        'setuptools-git',
    ],
    license='MIT',
    description='Lib para gerar arquivo TXT de tamanho fixo',
    long_description=open('README.md', 'r').read(),
    download_url='https://github.com/Trust-Code/python-cnab',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    tests_require=[
        'mock',
    ],
)
