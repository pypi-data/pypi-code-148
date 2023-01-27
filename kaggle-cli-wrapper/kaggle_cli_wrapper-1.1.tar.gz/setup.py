from distutils.core import setup
from setuptools import find_packages


setup(
    name="kaggle_cli_wrapper",
    description='Kaggle CLI Wrapper',
    version=1.1,
    long_description=('Wrapper over Kaggle official API for ease of use '
    'while downloading competition datasets and general datasets.'
    ),
    url="https://github.com/sunny1401/kaggle_utils",
    author="Sunny Joshi",
    author_email="sunnyjoshi1401@gmail.com",
    packages=(find_packages()+find_packages(where="./kaggle_cli_wrapper"))
)
