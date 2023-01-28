from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["click", "click-aliases", "requests", "parsedatetime", "python-dateutil"]

setup(
    name="vja",
    version="0.0.2",
    author="Christoph Ernst",
    author_email="christoph.ernst72@googlemail.com",
    description="A simple CLI for Vikunja task manager",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ce72/vja/",
    packages=find_packages(),
    install_requires=requirements,
    scripts=[
          'vja/vja',
      ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ]
)