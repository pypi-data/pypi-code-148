from setuptools import setup

setup(
    name='abork_logger',
    version='1.0.6',
    author='Alex Bork',
    packages=['logger'],
    description='Logging Library',
    install_requires=['colorama==0.4.5', 'termcolor==1.1.0']
    )