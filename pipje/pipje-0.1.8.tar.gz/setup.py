from setuptools import setup, find_packages
import codecs
import os
VERSION = "0.1.8"
DESCRIPTION = "Pipje was intended as a joke, it shows an image of a cat named pip by default."
LONG_DESCRIPTION = "Hi, you can use pipje like this to display any image you would like. The function is: showimage(TITLE,URL)"
# Setting up
setup(
    name="pipje",
    version=VERSION,
    author="Hurbie48 (Matthijs Veldkamp)",
    author_email="<matjepatatje2@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['tk','pillow','urlopen'],
    keywords=["python", "tkinter", "cat"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)