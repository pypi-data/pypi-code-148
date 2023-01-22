import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name='Topsis-Shrey-102183040',
    version="1.0.4",
    description="Compute Topsis scores and ranks for a given csv file using topsis method for multiple-criteria decision making(MCDM) ",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ShreySaxena24/Topsispy",
    author="Shrey Saxena",
    author_email="shrey.saxena.sms@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=['Topsis-Shrey-102183040'],
    include_package_data=True,
    install_requires=find_packages(),
    entry_points={
        "console_scripts": [
            "topsis=topsisfile.__main__:topsis",
        ]
    },
)