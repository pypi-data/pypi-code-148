import sys
import os
import setuptools

sys.path[0:0] = ['curvenote']
from version import __version__

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="curvenote",
    description="Helper library from Curvenote for data science in Jupyter notebooks",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
    ],
    url="http://curvenote.com",
    version=__version__,
    author="Curvenote inc.",
    author_email="hi@curvenote.com",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "ipython",
        "pandas",
        "traitlets",
        "ipywidgets"
    ],
    python_requires=">=3.7",
)
