from setuptools import find_packages, setup

setup(
    name="doml_synthesis",
    packages=find_packages(exclude=['tests']),
    version='1.0.0',
    description="This library allows to synthetize a new DOML from an existing one, following user-specified requirements",
    author='Andrea Franchini',
    author_email='hello@andreafranchini.com',
    license='MIT',
    install_requires=['z3-solver'],
    test_suite='tests'
)
