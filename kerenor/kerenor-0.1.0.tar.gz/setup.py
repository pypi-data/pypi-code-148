from setuptools import setup, find_namespace_packages

PROJECT = "kerenor"

setup(
    name=PROJECT,
    version='0.1.0',
    description=PROJECT,
    author=PROJECT,
    package_data={PROJECT: ["./imgs/*"]},
    include_package_data=True,
    packages=find_namespace_packages(include=[f"{PROJECT}*"])
)
