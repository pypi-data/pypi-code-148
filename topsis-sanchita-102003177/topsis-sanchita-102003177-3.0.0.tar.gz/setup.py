import pathlib
from setuptools import setup,find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="topsis-sanchita-102003177",
    version="3.0.0",
    description="It finds the topsis and rank of an input file",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SanchitaBora/topsis-102003177",
    author="Sanchita Bora",
    author_email="sbora_be20@thapar.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    # entry_points={
    #     "console_scripts": [
    #         "topsis=topsis-sanchita-102003177.102003177:main",
    #     ]
    # },
)