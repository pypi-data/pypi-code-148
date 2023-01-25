"""
Author: Eric Pace
This file is part of dicom_anonymiser.

dicom_anonymiser is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation version 3.

dicom_anonymiser is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with Patient CT Contour.
If not, see <https://www.gnu.org/licenses/>.
"""


import setuptools
from pathlib import Path

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Eric Pace",
    author_email="ericpace@pm.me",
    name='dicom_anonymiser',
    license="GNU GPLv3",
    description='dicom_anonymiser anonymises dicom files and folders with user customisable tags.',
    version='v0.2.4',
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url='https://github.com/ericpace/dicom_anonymiser',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'anonymise=dicom_anonymiser.__main__:main'
        ]
    },
    python_requires=">=3.8",
    # Enable install requires when publishing on the normal PyPi
    install_requires=[
        'pydicom'],
    classifiers=[
        'Development Status :: 4 - Beta',
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)