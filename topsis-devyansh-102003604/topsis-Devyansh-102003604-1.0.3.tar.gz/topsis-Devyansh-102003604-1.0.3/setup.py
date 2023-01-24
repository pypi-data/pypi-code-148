from setuptools import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="topsis-Devyansh-102003604",
    version="1.0.3",
    author="Devyansh Bansal",
    author_email="dbansal5_be20@gmail.com",
    description="Calculating topsis score and finding rank",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/DEV7814/topsis-Devyansh-102003604",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={'': 'src'},
    py_modules=['topsis-Devyansh-102003604'],
    include_package_data=True,
    # install_requires=['pandas', 'numpy', 'os'],

)
