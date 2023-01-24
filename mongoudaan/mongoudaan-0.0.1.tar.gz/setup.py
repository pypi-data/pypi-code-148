from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'mongodb file storing'
LONG_DESCRIPTION = 'A package which can be used to store files on mongodb'
# Setting up
setup(
    name="mongoudaan",
    version=VERSION,
    author="Sahil Apte",
    author_email="sahilapte1@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['store files', 'database', 'store', 'file', 'sahil','mongo'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)