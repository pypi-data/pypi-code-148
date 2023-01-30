from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="filter strings",
    version="0.0.2",
    author="Jay Trairat",
    author_email="jaytrairat@outlook.com",
    description="",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jaytrairat/python-filter-strings",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
