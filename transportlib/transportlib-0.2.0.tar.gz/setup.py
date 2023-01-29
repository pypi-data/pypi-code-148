"""Minimal setup file for tasks project."""

from setuptools import setup, find_packages


def get_requires():
    required = []

    print()
    with open('requirements.txt', 'r') as f:
        required = f.read().splitlines()

    return required


setup(
    name='transportlib',
    version='0.2.0',
    python_requires='>=3.7',
    license='proprietary',
    description='A library for reusable transport utilities',
    author='Ken Ho',
    author_email='kenho811@gmail.com',

    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=get_requires(),

)
