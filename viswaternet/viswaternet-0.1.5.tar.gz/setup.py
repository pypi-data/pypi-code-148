#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pandas',
               'numpy',
               'matplotlib>=3.3.0',
               'wntr',
               'imageio',
               'networkx']

test_requirements = [ ]

setup(
    author="Tyler Trimble",
    author_email='TylerL.Trimble@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A python package for easy generation and customization of water network graphs.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='viswaternet',
    name='viswaternet',
    packages=find_packages(include=['viswaternet', 'viswaternet.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tylertrimble/viswaternet',
    version='0.1.5',
    zip_safe=False,
)
