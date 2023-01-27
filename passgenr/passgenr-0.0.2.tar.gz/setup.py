from setuptools import setup, find_packages
import os
import codecs

VERSION = '0.0.2'
DESCRIPTION = "a random password generator build with basic python coding"
LONG_DESC = '''In the function we have to provide values as: 
passgenr(n_letter, n_digit, n_symbol) 
to get the randomly generated string'''

# setting up module
setup(
    name='passgenr',
    version=VERSION,
    author="Coder014 (Chandan Kumar)",
    author_email="binary.commands@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESC,
    packages=find_packages(),
    requires=[],
    keywords=['python', 'random', 'password generator', 'password'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)
