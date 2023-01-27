#!/usr/bin/env python

from setuptools import find_packages, setup


def read_file(file_path):
    return open(file_path, "r", encoding="utf-8").read()


setup(
    name="parsing_steps",
    version="0.0.2",
    url="https://github.com/loievskyi/parsing_steps",
    license="Apache Software License",
    description="A simple helper for data parsing.",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Viacheslav Loievskyi",
    author_email="loievskyi.slava@gmail.com",
    packages=find_packages(exclude=["tests*", "parsing_steps/future*", "old_code/*"]),
    include_package_data=True,
    python_requires=">=3.8",
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    project_urls={
        "Source": "https://github.com/loievskyi/parsing_steps",
    },
)
