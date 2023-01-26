#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JiansuoJishuHexin20jiang
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JiansuoJishuHexin20jiang'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="jiansuo-jishu-hexin-20jiang",
    version=JiansuoJishuHexin20jiang.__version__,
    url="https://github.com/apachecn/jiansuo-jishu-hexin-20jiang",
    author=JiansuoJishuHexin20jiang.__author__,
    author_email=JiansuoJishuHexin20jiang.__email__,
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
    description="123-检索技术核心20讲",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "jiansuo-jishu-hexin-20jiang=JiansuoJishuHexin20jiang.__main__:main",
            "JiansuoJishuHexin20jiang=JiansuoJishuHexin20jiang.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
