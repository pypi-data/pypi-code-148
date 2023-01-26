#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import QuanzhanGongchengshiXiulianZhinan
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('QuanzhanGongchengshiXiulianZhinan'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="quanzhan-gongchengshi-xiulian-zhinan",
    version=QuanzhanGongchengshiXiulianZhinan.__version__,
    url="https://github.com/apachecn/quanzhan-gongchengshi-xiulian-zhinan",
    author=QuanzhanGongchengshiXiulianZhinan.__author__,
    author_email=QuanzhanGongchengshiXiulianZhinan.__email__,
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
    description="87-全栈工程师修炼指南",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "quanzhan-gongchengshi-xiulian-zhinan=QuanzhanGongchengshiXiulianZhinan.__main__:main",
            "QuanzhanGongchengshiXiulianZhinan=QuanzhanGongchengshiXiulianZhinan.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
