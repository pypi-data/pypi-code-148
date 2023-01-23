from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="alphahutch",
    version="0.0.4",
    description="Common packages that will be used for alphahutch",
    long_description=long_description,
    author="Andy Hutchinson",
    url="https://github.com/HutchNunez/alphahutch",
    packages=find_packages(),
    install_requires=["elasticsearch==7.13.1", "pandas==1.5.2"],
)
