from setuptools import setup 
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(name="Topsis_Aashutosh_102053043",version="0.5",
description="This is a topsis package of version 0.5",
long_description=long_description,
    long_description_content_type="text/markdown",
author="Aashutosh Dubey",
author_email="asaashutoshdubey0@gmail.com",
packages=['Topsis_Aashutosh_102053043'],
install_requires=['pandas'],
include_package_data=True,
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Aashutosh_102053043.Aashutosh_102053043:main",
        ]
    }
)