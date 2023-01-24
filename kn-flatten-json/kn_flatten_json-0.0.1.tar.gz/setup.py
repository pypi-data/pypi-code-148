from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'kn_flatten_json'
LONG_DESCRIPTION = 'A package to flatten a dataframe containing complex datatypes'

# Setting up
setup(
    name="kn_flatten_json",
    version=VERSION,
    author="Sukriti",
    author_email="sukriti.saluja@kockpit.in",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['flatten', 'json', 'normalize', 'normalize pyspark dataframe', 'complex datatypes', 'flatten dataframe'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
