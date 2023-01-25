from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='py-chan-calculator',
    version='0.0.2',
    description='This is a simple calculator package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ChanduArepalli/py-chan-calculator',
    author='Chandu Arepalli',
    author_email='chandumanikumar4@gmail.com',
    license='BSD 2-clause',
    packages=['pychancalculator'],
    install_requires=[],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)