from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_Sudhit_102017137",version="0.1",
description="This is a topsis package of version 0.1",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Sudhit Soni",
author_email="soni_be20@thapar.edu",
packages=['Topsis_Sudhit_102017137'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Sudhit_102017137.Sudhit_102017137:main",
        ]
    }
)