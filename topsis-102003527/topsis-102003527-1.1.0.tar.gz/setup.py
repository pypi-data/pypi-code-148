from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1.0'
DESCRIPTION = 'It evaluates alternatives based on multiple criteria using TOPSIS method'

# Setting up
setup(
    name="topsis-102003527",
    version=VERSION,
    author="Aarushi Abrol",
    author_email="<aabrol_be20@thapar.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/aarushi353/Topsis",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)