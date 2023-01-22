from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Multi-Criteria Decision Making'
LONG_DESCRIPTION = 'A package to rank the models on the basis of TOPSIS method'


# Setting up
setup(
    name="Topsis-Twesha-102017195",
    version=VERSION,
    author="Twesha",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license="MIT",
    packages=["topsis"],
    install_requires='pandas',
    include_package_data=True,
    keywords=['python', 'best model', 'Topsis', 'multi-criteria decision making', 'assignment'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    
    # This is necessary to get the executable file (topsis here) which acts as a command initiater. If entry point is not mentioned then
    # we would not be able to use the command as executable file is not created. 
    #If we change the name from 'topsis' to some other name then that name would be used to access the executable file.
    entry_points={
        "console_scripts": [
            "topsis=topsis.topsis:main",
        ]
    },
)
