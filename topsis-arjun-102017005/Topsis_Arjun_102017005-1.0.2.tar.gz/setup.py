from setuptools import setup, find_packages
import pathlib
import codecs
import os

HERE = pathlib.Path(__file__).parent
VERSION = '1.0.2'
DESCRIPTION = 'A Python package for Multiple Criteria Decision Analysis (MCDA) using TOPSIS Method made by Arjun Khanchandani.'
LONG_DESCRIPTION = README = (HERE / "README.md").read_text()

# Setting up
setup(
    name="Topsis_Arjun_102017005",
    version=VERSION,

    author="Arjun Khanchandani",
    author_email="<akhanchandani_be20@thapar.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'topsis', 'mcda'],

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            "Topsis-Arjun-10207005=Topsis_Arjun_102017005.__init__:main",
        ],
    }
)