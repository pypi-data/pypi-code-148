import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="fxitility",
    version="0.0.2",
    author="Jonel Agustin Mawirat",
    author_email="jmawirat@fivetalents.capital",
    description="Forex Utility Package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/jmawirat/fxitility",
    keywords="Forex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent" 
    ]
)