# setup.py
from keyring import get_keyring
get_keyring()
from setuptools import setup

setup()

# Using bumpver we can automatically
# version our library
# to install: python -m pip install bumpver
# bumpver init
# bumpver update --minor

# python -m pip install build twine

# python -m build
