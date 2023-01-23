from setuptools import setup, find_packages

with open("readme.txt", "r") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Manpreet-102003171",
    version="0.0.3",
    author="Manpreet Singh",
    author_email="manpreetchahal0786@gmail.com",
    description="Calculates Topsis Score and Rank them accordingly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires='pandas',
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main"
        ]
    },
)