from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.1'
DESCRIPTION = 'ElGamal encryption module'

# Setting up
setup(
    name="elgamal-anass-daniel",
    version=VERSION,
    author="Anass Anhari & Daniel Alamillo",
    author_email="<anassanhari@estudiantat-upc.edu>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'elgamal', 'encryption', 'chyper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)