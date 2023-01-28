import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="lazyeval", 
    version="0.0.3",
    author="Kim Hyun Bin",
    author_email="KIMH0004@e.ntu.edu.sg",
    description="A python package to automate machine learning process to showcase metric values in an instance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanilladucky/ModelExploration",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)