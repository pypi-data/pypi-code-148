from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'A game engine based on pygame. It allows you to make your own games.'

# Setting up
setup(
    name="pywingame",
    version=VERSION,
    author="JacksonLin (JacksonLin)",
    author_email="jacksonlam.macau@outlook.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pygame', 'clipboard'],
    keywords=['python', 'game', 'game engine'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)