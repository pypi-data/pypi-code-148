import setuptools

long_description = open("README.md", "r").read()
requirements = [i.strip() for i in open("requirements.txt", "r").readlines()]

setuptools.setup(
    name="fvscraper",
    version="0.0.1",
    author="Daniel Ik",
    description="Library for interacting with https://finviz.com",
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    py_modules=["finscraper"],
    package_dir={"":"."},
    install_requires=requirements
)