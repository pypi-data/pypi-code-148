import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Topsis-Sidak-102003649",
    version="1.0.3",
    description="Compute Topsis Scores/Ranks of a given csv file",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://https://github.com/sidak2609/topsis",
    author="Sidak Khotra",
    author_email="sidakkhotra@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["Topsis-Sidak-102003649"],
    include_package_data=True,
    install_requires=find_packages(),
    entry_points={
        "console_scripts": [
            "topsis=topsisfile.__main__:topsis",
        ]
    },
)