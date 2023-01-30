#!/usr/bin/env python3
"""
Numpy build options can be modified with a site.cfg file.
See site.cfg.example for a template and more information.
"""

import os
from pathlib import Path
import setuptools
import sys


def setup_package():
    package_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    setup_params = dict(
        name=package_name,
        version='0.0.5',
        maintainer='Mathew Stylianidis',
        description='All-around utility functions for the Python programmer.',
        long_description=Path('README.md').read_text(encoding='utf-8'),
        long_description_content_type='text/markdown',
        author='Mathew Stylianidis',
        download_url=f'https://pypi.python.org/pypi/{package_name}',
        project_urls={
            "Bug Tracker": f'https://github.com/MathewStylianidis/{package_name}/issues',
            "Source Code": f'https://github.com/MathewStylianidis/{package_name}',
        },
        license='MIT License',
        classifiers=[
            "Programming Language :: Python :: 3.9",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        test_suite='pytest',
        python_requires='>=3.9',
    )
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    setup_package()

