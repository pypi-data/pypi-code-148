from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.3'
DESCRIPTION = 'Take the Reptiviness out of File Reading / Writing'

# Setting up
setup(
    name="fjunkie",
    version=VERSION,
    author="GalaxyIndieDev",
    author_email="<zachnichelson304@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['api', 'file', 'read', 'write', 'utils'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)