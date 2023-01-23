
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis-Karanjot-102003257",
    version="1.0.1",
    author="Karanjot Singh",
    author_email="ksingh5_be20@thapar.edu",
    description="A package -> Calculates Topsis Score and Rank them accordingly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["TOPSIS_Calc_102003257"],
    include_package_data=True,
    install_requires='pandas',
    entry_points={
        "console_scripts": [
            "topsis=TOPSIS_Calc_102003257.102003257:main",
        ]
    },
)