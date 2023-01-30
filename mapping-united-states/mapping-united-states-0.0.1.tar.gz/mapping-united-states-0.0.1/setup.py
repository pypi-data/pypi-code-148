#!/usr/bin/env python
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mapping-united-states",
    version="0.0.1",
    author="pixel-coding-studio",
    description="Mapping United States is a mapping tool that utilizes the census shape files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pixel-coding-studio/mapping-united-states",
    project_urls={

    },
    classifiers=[],
    package_dir={"": "mapping_united_states"},
    python_requires=">=3.6",
    license="MIT",
    packages=setuptools.find_packages(where="mapping_united_states"),
    install_requires=[
        "geopandas>=0.12.2",
        "matplotlib>=3.6.3",
        "pandas>=1.5.3",
        "requests>=2.28.2",
        "tqdm>=4.64.1"
    ],
)
