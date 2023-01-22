from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Topsis package- Pranjal Arora'


# Setting up
setup(
    name="Topsis-Pranjal-102003402",
    version=VERSION,
    author="Pranjal Arora",
    author_email="<prv.gma@gmail.com>",
    url='https://github.com/pranjal-arora/Topsis',
    download_url='https://github.com/pranjal-arora/Topsis/archive/refs/tags/v_01.tar.gz',
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'logging'],
    keywords=['python', 'topsis', 'machinelearning', 'datascience', 'statistics', 'predictiveanalysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)