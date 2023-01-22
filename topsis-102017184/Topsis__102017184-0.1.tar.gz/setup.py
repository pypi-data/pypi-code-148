from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.-0'
DESCRIPTION = 'Topsis Package'

# Setting up
setup(
    name="Topsis-102017184",
    version=0.1,
    author="Ishita Kaundal",
    author_email="ikaundal_be20@thapar.edu",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)