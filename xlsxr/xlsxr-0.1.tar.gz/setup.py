#!/usr/bin/python

from setuptools import setup
import sys

if sys.version_info < (3,):
    raise RuntimeError("xlsx-reader requires Python 3 or higher")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='xlsxr',
    version="0.1",
    description="Read very large Excel XLSX files efficiently",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='David Megginson',
    author_email='megginson@un.org',
    install_requires=['requests',],
    packages=['xlsxr',],
    test_suite='tests'
)
