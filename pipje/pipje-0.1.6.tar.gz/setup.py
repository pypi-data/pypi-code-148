from setuptools import setup, find_packages
import codecs
import os
VERSION = "0.1.6"
DESCRIPTION = "Pipje was intended as a joke, it shows an image of a cat named pip by default.\nBut, you can use pipje like this to display any image you would like.:\nshowimage(TITLE,URL)"
# Setting up
setup(
    name="pipje",
    version=VERSION,
    author="Hurbie48 (Matthijs Veldkamp)",
    author_email="<matjepatatje2@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['tk','pillow','urlopen','sys'],
    keywords=["python", "tkinter", "cat"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)