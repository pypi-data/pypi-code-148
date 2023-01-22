import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TOPSIS-Sahil_Rohilla-102183056",
    version="1.0.4",
    # package_dir={'':'TOPSIS_Sahil'},
    py_modules=["TOPSIS"],
    author="Sahil",
    author_email="ssahil1_be20@thapar.edu",
    description="A Topsis package that takes inputs as CSV and generates scores in results CSV!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SahilRo/TOPSIS-Sahil-102183056",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.18.1",
        "pandas>=1.0.5"
    ],
)