"""Setup file for Python lib."""
from setuptools import setup, find_packages
import pathlib

__name__ = "jade-md"
__version__ = "0.0.3"
__description__ = "Jade - A Python library for rendering markdown to HTML for Flask."

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    url="https://github.com/sam-kenney/jade",
    author="Sam Kenney",
    author_email="sam.kenney@me.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=[],
    install_requires=[
        "flask==2.2.2",
        "jinja2==3.1.2",
        "markdown==3.4.1",
        "pyyaml==6.0",
    ],
    packages=["jade"] + ["jade." + pkg for pkg in find_packages("jade")],
)
