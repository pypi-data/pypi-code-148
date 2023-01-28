from setuptools import setup

with open('README.md','r') as fh:
    long_description = fh.read()

setup(
    name = 'helperagent',
    version='2.0.0',
    description='somepackage',
    py_modules=["helperagent"],
    install_requires = [
        'pandas',
        'numpy',
        'matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require={
        "dev":[
            "pytest",
        ],
    },
)