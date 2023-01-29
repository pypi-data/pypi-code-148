import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='qoalarandom',version='1.0.5',scripts=['qrandom'] ,
     author="Qoalas Team",
     author_email="hannah.yelle@maine.edu",
     description="iQuHack 2023, CovalentxIBM Challenge",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/iQuHack-2023-Qoalas/qRandom.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",])

 