import os

from setuptools import setup, find_packages

setup(
    name='peolymp',
    version=os.getenv("RELEASE_VERSION"),

    url='https://github.com/ukroi',
    author='Anton Tsypko',
    author_email='tsypko@oi.in.ua',

    packages=find_packages(),

    install_requires=[
        'eolymp',
        'requests',
        'protobuf'
    ],
)
