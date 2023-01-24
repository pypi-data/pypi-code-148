from setuptools import setup, find_packages
with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name = "manini",
    version = "0.0.2",
    description = "An user-friendly plugin that enables to annotate images from a pre-trained model (segmentation, classification, detection) given by an user.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/hereariim/manini",
    packages=find_packages(),
    author = "Herearii Metuarea",
    author_email = "herearii.metuarea@gmail.com",
    license = "BSD-3-Clause",
    license_files = "LICENSE",
    classifiers =[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: napari",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
install_requires = [
    "numpy",
    "magicgui",
    "qtpy",
    "napari",
    "magicgui",
    "scikit-image",
    "numpy",
    "pandas",
    "opencv-python-headless",
    "tensorflow",
    "PyQt5"
],
python_requires = ">=3.8",
)