from setuptools import setup, find_packages
import codecs
import os
VERSION = "0.1.2"
DESCRIPTION = "Pipje was intended as a joke, it shows an image of a cat named pip."
# Setting up
setup(
    name="pipje",
    version=VERSION,
    author="Hurbie48 (Matthijs Veldkamp)",
    author_email="<matjepatatje2@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=["tk", "os", "system","time"],
    keywords=["python", "tkinter", "cat"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)