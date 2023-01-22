from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_Sarisha_102003445",version="0.7",
description="This is a topsis package of version 0.7",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Aditya Singh Rathore",
author_email="saggarwal4_be20@thapar.edu",
packages=['Topsis_Sarisha_102003445'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Sarisha_102003445.Sarisha_102003445:main",
        ]
    }
)