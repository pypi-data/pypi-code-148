from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="filter-strings",
    version="0.0.10",
    author="jaytrairat",
    author_email="jaytrairat@outlook.com",
    description="Filter strings from a file based on regex patterns.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/jaytrairat/python-filter-strings",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'filter-strings = filter_strings.main:main',
        ],
    },
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
