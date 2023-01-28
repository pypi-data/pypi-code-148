"""Python setup.py for package"""
import io
import os

from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [line.strip() for line in read(path).split("\n") if not line.startswith(('"', "#", "-", "git+"))]


setup(
    name="Genr",
    version="0.0.1",
    description="A library to cater all your NLP tasks using LLMs",
    url="https://github.com/psytech42/genr.ai",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author='manomay-psytech',
    packages=find_packages(),
    install_requires=read_requirements("/home/manomay/Desktop/PsyTech/genr.ai/requirements.txt"),
    python_requires=">=3.7.0",
)
