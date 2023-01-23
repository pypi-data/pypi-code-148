from setuptools import setup
def readme():
    with open('Readme.md.txt') as f:
        Readme = f.read()
    return Readme

setup(
name="packageharman",
version="0.2",
description='This is a Python Package implementing TOPSIS used for multi-criteria decision analysis method',
long_description=readme(),
author="Harmanjot Kaur",
author_email='hkaur4_be20@thapar.edu',
packages=['packageharman'],
install_requires=['numpy','pandas']

)