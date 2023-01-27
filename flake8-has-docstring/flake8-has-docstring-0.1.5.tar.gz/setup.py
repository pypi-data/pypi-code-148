from setuptools import setup

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read().strip()

setup(
    name="flake8-has-docstring",
    version="0.1.5",
    python_requires=">=3.10,<3.11",
    install_requires=install_requires,
    py_modules=["flake8_has_docstring"],
    entry_points={"flake8.extension": "DOC001 = flake8_has_docstring:Plugin"},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
