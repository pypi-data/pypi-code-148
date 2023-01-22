from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A TOPSIS python Package'
LONG_DESCRIPTION = 'A Python package implementing Topsis method for multi-criteria decision analysis.'

# Setting up
setup(
    name="Topsis_102017189",
    version=VERSION,
    author="Vishalakshi",
    author_email="vishalakshik02@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'sys'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "Topsis_102017189=topsis.cli:main",
        ]
    },
)