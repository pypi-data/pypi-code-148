from setuptools import find_packages, setup

_MAJOR = "1"
_MINOR = "4"
_UNDER_MINOR = "2"

VERSION_SHORT = f"{_MAJOR}.{_MINOR}.{_UNDER_MINOR}"
VERSION = f"{_MAJOR}.{_MINOR}.{_UNDER_MINOR}"

with open("requirements.txt") as f:
    requirements = list(line.strip() for line in f.readlines())

setup(
    name="vtorch",
    packages=find_packages(),
    include_package_data=True,
    version=VERSION,
    description="NLP research library, built on PyTorch.",
    author="Paul Khudan, Ilya Strelnikov, Vitalii Koren, Vitalii Radchenko",
    author_email="ds@youscan.io",
    install_requires=requirements,
)
