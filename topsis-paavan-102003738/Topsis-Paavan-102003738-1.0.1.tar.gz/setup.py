import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name='Topsis-Paavan-102003738',
    version="1.0.1",
    description="Calculate topsis score and rank and evaluate.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Paavan75/Topsis",
    author="Paavan Singh Sayal",
    author_email="paavan.sayal@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=['Topsis-Paavan-102003738'],
    include_package_data=True,
    install_requires=find_packages(),
    entry_points={
        "console_scripts": [
            "topsis=topsisfile.__main__:topsis",
        ]
    },
)