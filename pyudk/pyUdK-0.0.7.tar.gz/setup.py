"""Python setup.py for pyUdK package"""
import io
import os
from setuptools import find_packages, setup

VERSION = '0.0.7'


def read(*paths, **kwargs):
    """Read the contents of a text file safely. >>> read("project_name", "VERSION")
    '0.1.0' >>> read("README.md") ..."""
    content = ""
    with io.open(
            os.path.join(os.path.dirname(__file__), *paths),
            encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="pyUdK",
    version=VERSION,
    description="Computes Udwadia–Kalaba constraint forces of an "
                "equation of motion of a constrained mechanical system.",
    url="https://github.com/Eddy-Morgan/PyUdK",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Edward Morgan",
    author_email='emorg31@lsu.edu',
    license='MIT',
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    keywords=['python', 'pyUdK', 'Udwadia Kalaba', 'constraint', 'gaussian', 'equation of motion',
              'constrained mechanical system'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering"
    ]
)
