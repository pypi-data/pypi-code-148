import setuptools
from setuptools import setup, find_packages



with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pyMicroCode",
    version = "7.0.0",
    author = "Cactochan",
    packages=find_packages('src'),
    package_dir={'': 'src'},
description = "generate microcode(these are sort of like qrcode but have someother uses)",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/mastercodermerwin/pyMicroCode",
    project_urls = {
        "Bug Tracker": "https://github.com/mastercodermerwin/pyMicroCode/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
