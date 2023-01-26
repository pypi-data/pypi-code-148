#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import SpringBianchengChangjianCuowu50li
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('SpringBianchengChangjianCuowu50li'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="spring-biancheng-changjian-cuowu-50li",
    version=SpringBianchengChangjianCuowu50li.__version__,
    url="https://github.com/apachecn/spring-biancheng-changjian-cuowu-50li",
    author=SpringBianchengChangjianCuowu50li.__author__,
    author_email=SpringBianchengChangjianCuowu50li.__email__,
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
    description="188-Spring编程常见错误50例",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "spring-biancheng-changjian-cuowu-50li=SpringBianchengChangjianCuowu50li.__main__:main",
            "SpringBianchengChangjianCuowu50li=SpringBianchengChangjianCuowu50li.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
