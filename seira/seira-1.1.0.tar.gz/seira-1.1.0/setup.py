from setuptools import setup, find_packages
import codecs
import os
from pathlib import Path

VERSION = '1.1.0'
DESCRIPTION = 'SEIRA: DATA PROCESSING FOR SEISMIC REFRACTION AND MASW'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Setting up
setup(
    name="seira",
    version=VERSION,
    author="Putu Pradnya Andika, Tedi Yudistira",
    author_email="<putuandhika@hotmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords=['python', 'seismic refraction tomography', 'masw'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)