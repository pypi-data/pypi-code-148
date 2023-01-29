import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
fh.close()

setuptools.setup(
    name="calculator_cwl",
    version="1.2",
    author="CodeWithLaksh",
    author_email="dashlakshyaraj2006@gmail.com",
    description="A Python Package Which does basic math calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codewithlaksh/calculator_cwl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)