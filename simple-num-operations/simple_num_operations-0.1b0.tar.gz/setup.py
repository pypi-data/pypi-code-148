from setuptools import setup

with open("README.md") as file:
    read_me_description = file.read()

setup(
    name="simple_num_operations",
    version="0.1beta",
    author="thedotaxein",
    author_email="axeinthereal@gmail.com",
    description="This is a package to do some operations with numbers.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thedotaxein/simplenumoperations",
    packages=['simple_num_operations'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'colorama',
    ],
    python_requires='>=3.9',
)
