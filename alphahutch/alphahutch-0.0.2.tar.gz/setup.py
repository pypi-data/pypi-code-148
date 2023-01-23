from setuptools import setup, find_packages

setup(
    name="alphahutch",
    version="0.0.2",
    description="Common packages that will be used for alphahutch",
    long_description="Common packages that will be used for alphahutch",
    author="Andy Hutchinson",
    url="https://gitlab.com/data168/alphahutch/-/tree/master/",
    author_email="andresuconunez@gmail.com",
    packages=find_packages(),
    install_requires=['elasticsearch==7.13.1'],
)