import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Ikshit-102003403",
    version="1.1.1",
    description="Implements topsis on the given input data file and generates topsis score and ranks accordingly.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ikshit2809/Topsis",
    author="Ikshit",
    author_email="iikshit_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=['pandas','sys','os','math'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)