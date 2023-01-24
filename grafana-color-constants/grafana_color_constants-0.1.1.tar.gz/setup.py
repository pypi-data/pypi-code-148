"""
Author: Calixte Mayoraz
Copyright: Eversys SA
Created: 2023-01-23
"""
"""SetupTools configuration"""
import setuptools
from m2r import convert


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()  # markdown to RST conversion for PyPi


setuptools.setup(
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "src"},  # the start of the code folder
    packages=setuptools.find_packages(where="src"),
    setuptools_git_versioning={
        "enabled": True,
        "template": "{tag}",
        "dirty_template": "{tag}"
    },
    setup_requires=["setuptools-git-versioning"],
    python_requires=">=3.7",
    install_requires=[
        "m2r==0.2.1"
    ]
)