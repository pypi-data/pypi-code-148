import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Setting up
setup(
    name="GRLMerger",
    version='0.0.33',
    description='GRL Merger is a package that allows to merge two GRL models that are written in TGRL syntax into one GRL model.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['grlmerger'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        'pandas', 
        'numpy',
        'statistics',
        'neattext',
        'nltk',
        'sentence_transformers',
        'openpyxl',
        'xlsxwriter',
    ],
    author="Nadeen AlAmoudi",
    author_email="<nadeenamoudi1@gmail.com>",
#    packages = setuptools.find_packages(where="src"),
)