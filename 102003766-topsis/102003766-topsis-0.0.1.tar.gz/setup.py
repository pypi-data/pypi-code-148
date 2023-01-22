from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = '102003766-topsis',
    version = '0.0.1',
    description='Multiple Criteria Decision Making',
    py_modules=['topsis'],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author = "Sahil Chhabra",
    author_email="sahil.chh718@gmail.com",
)