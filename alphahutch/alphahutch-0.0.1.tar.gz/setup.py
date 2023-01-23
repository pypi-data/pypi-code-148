from setuptools import setup, find_packages

setup(
    name="alphahutch",
    version="0.0.1",
    description="Common packages that will be used for alphahutch",
    packages=find_packages(),
    install_requires=['elasticsearch==7.13.1'],
)