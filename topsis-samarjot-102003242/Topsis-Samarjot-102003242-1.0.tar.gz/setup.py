from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
    name="Topsis-Samarjot-102003242",
    version="1.0",
    description="Python package implementing TOPSIS multi-criteria decision making method.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Samarjot Singh",
    author_email="2001samar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["Topsis"],
    include_package_data=True,
    install_requires=['numpy',
                      'pandas',
     ],
     entry_points={
        "console_scripts": [
            "topsis=Topsis.__main__:main",
        ]
     },
)