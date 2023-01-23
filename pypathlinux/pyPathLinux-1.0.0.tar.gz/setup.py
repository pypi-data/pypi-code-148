import setuptools
from setuptools import setup, find_packages



with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pyPathLinux",
    version = "1.0.0",
    author = "Cactochan",
    packages=find_packages('src'),
    package_dir={'': 'src'},
description = "For path related stuff on linux..",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/mastercodermerwin/pypath",
    project_urls = {
        "Bug Tracker": "https://github.com/mastercodermerwin/pypath/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
