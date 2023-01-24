from setuptools import find_packages, setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='matplotlib-polyroi',
    version='0.1.3',
    license="CC BY 4.0",
    author='Tom Bland',
    author_email='tom_bland@hotmail.co.uk',
    packages=find_packages(),
    install_requires=['numpy',
                      'matplotlib',
                      'scipy',
                      'ipywidgets',
                      'scikit-image',
                      'jupyter'],
    description='Python implementation of SAIBR: a tool for performing spectral autofluorescence correction on biological images',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
