import setuptools
from setuptools import setup, find_packages



with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pyE2EE",
    version = "5.0.4",
    author = "Cactochan",
    packages=find_packages('src'),
    package_dir={'': 'src'},
description = "End To End Encryption in Python.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/mastercodermerwin/OSOME-DB",
    project_urls = {
        "Bug Tracker": "https://github.com/mastercodermerwin/OSOME-DB/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
