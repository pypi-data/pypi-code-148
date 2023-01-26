import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eukfindertest",
    version="1.2.3",
    author="dzhao,dsalas",
    author_email="dandan.tanny.zhao@email.com, dayana.salas.leiva@gmail.com",
    description="A small demo package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dzhao2019/Eukfinder",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)