#!/usr/bin/env python3
from setuptools import find_packages, setup

with open('chilli_py/version.py', 'r', encoding="utf-8") as fh:
    version = {}
    exec(fh.read(), version)

with open('README.md', 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='chilli_py',
    version=version['__version__'],
    description='A pure Python GTO SCF code.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/nextdft/chilli_py',
    author='Sebastian Schwalbe',
    author_email='theonov13@gmail.com',
    license='APACHE2.0',
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],
    extras_require={
        'addons': ['pyscf','basis_set_exchange']  
    },
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)

