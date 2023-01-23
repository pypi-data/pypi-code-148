from setuptools import find_packages, setup

setup(
    name='matplotlib-polyroi',
    version='0.1.1',
    license="CC BY 4.0",
    author='Tom Bland',
    author_email='tom_bland@hotmail.co.uk',
    packages=find_packages(),
    install_requires=['numpy',
                      'matplotlib',
                      'scipy',
                      'ipywidgets',
                      'scikit-image',
                      'jupyter']
)
