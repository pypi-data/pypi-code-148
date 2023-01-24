
from setuptools import setup, find_packages
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setup(
    name="xfsystem",
    version="0.0.2",
    author="Gwamaka Mwamwaja",
    author_email="gwamaka.mwamwaja@ucglobalprograms.org",
    packages=find_packages(),
    description="A package containing reusable functionalities for the mamba-spark project",
    url="https://github.com/GwamakaCharles/ucsf_xfsystem",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)