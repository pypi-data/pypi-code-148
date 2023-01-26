#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JavaXingnengTiaoyouShizhan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JavaXingnengTiaoyouShizhan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="java-xingneng-tiaoyou-shizhan",
    version=JavaXingnengTiaoyouShizhan.__version__,
    url="https://github.com/apachecn/java-xingneng-tiaoyou-shizhan",
    author=JavaXingnengTiaoyouShizhan.__author__,
    author_email=JavaXingnengTiaoyouShizhan.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="47-Java性能调优实战",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "java-xingneng-tiaoyou-shizhan=JavaXingnengTiaoyouShizhan.__main__:main",
            "JavaXingnengTiaoyouShizhan=JavaXingnengTiaoyouShizhan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
