from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_Aditya_102003424",version="0.8",
description="This is a topsis package of version 0.8",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Aditya Singh Rathore",
author_email="arathore_be20@thapar.edu",
packages=['Topsis_Aditya_102003424'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Aditya_102003424.Aditya_102003424:main",
        ]
    }
)