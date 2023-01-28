import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis_Puranjay_102003384",
    version="0.3.0",
    description="Python package to implement TOPSIS.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/purjaysin/topsis-Puranjay-102003384",
    author="Puranjay Singh",
    author_email="psingh12_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["topsis"],
    include_package_data=True,
    install_requires=["pandas", "numpy","tabulate"],
    entry_points={
        "console_scripts": [
            "Topsis_Puranjay_102003384=Topsis_Puranjay_102003384.__main__:main",
        ]
    },
)