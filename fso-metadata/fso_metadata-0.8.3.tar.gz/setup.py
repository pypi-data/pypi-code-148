from distutils.core import setup
from setuptools import setup

# read the contents of README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="fso_metadata",
    packages=["fso_metadata"],
    version="0.8.3",
    license="MIT",
    description="FSO metadata access automation. Seamless access to SMS 2.0 APIs in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pauline Maury Laribière, Lancelot Marti",
    author_email="pauline.maury-laribiere@bfs.admin.ch, lancelot.marti@bfs.admin.ch",
    url="https://renkulab.io/gitlab/pauline.maury-laribiere/meatadata-auto",
    download_url="https://renkulab.io/gitlab/pauline.maury-laribiere/meatadata-auto/-/archive/v_0.8/meatadata-auto-v_0.8.tar.gz",
    keywords=[
        "metadata",
        "automation",
        "open-data",
        "API",
        "SMS 2.0",
        "statistics",
        "IOP",
    ],
    install_requires=["openpyxl", "pandas", "pandasdmx"],
    classifiers=[
        "Development Status :: 3 - Alpha",  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
