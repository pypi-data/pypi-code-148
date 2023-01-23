import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis_Pranjal_102003623",
    version="1.0.1",
    description="This is a Python library for handling problems related to Multiple Criteria Decision Making(MCDM)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Pranjal283/Topsis_Pranjal_102003623",
    
    author="Pranjal Sharma",
    author_email="pranjal28sharma@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis_Pranjal_102003623"],
    include_package_data=True,
    install_requires="pandas",
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Pranjal_102003623.topsis:main",
        ]
    },
)