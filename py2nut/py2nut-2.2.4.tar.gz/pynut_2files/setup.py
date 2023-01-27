import pathlib
from setuptools import setup, find_packages
import pyNutFiles

# The text of the README file
ME_PATH = pathlib.Path(__file__).parent
README = (ME_PATH / "README.md").read_text()

# This call to setup() does all the work
setup(
    name    = "pynut-Files",
    version = pyNutFiles.__version__,
    description = "Function easing life :)",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Laurent-Tupin/pynut_Files",
    author = "Laurent Tupin",
    author_email = "laurent.tupinn@gmail.com",
    license = "Copyright 2022-2035",
    classifiers=[
        "License :: Free For Home Use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages = find_packages(exclude = ("test",)),
    include_package_data = True,
    install_requires = ["pynut-tools==2.2.5", "openpyxl==3.0.5", "psutil==5.9.0",
                        "pywin32==303", "xlrd==1.2.0", "XlsxWriter==1.3.5",
                        "xlwings==0.20.8"]
    #entry_points={"console_scripts": ["EXEnameFile=FolderName.__main__:main"]},
)
