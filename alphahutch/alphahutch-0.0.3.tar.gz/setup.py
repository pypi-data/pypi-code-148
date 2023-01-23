from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name="alphahutch",
    version="0.0.3",
    description="Common packages that will be used for alphahutch",
    long_description=long_description,
    author="Andy Hutchinson",
    url="https://github.com/HutchNunez/alphahutch",
    packages=find_packages(),
    install_requires=install_requires,
)
