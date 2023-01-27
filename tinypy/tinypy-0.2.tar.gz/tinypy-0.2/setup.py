from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tinypy",
    version=0.2,
    description="A library for handling files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Arash Yeganeh",
    packages=find_packages(),
    url="https://github.com/arashyeganeh/tinypy",
    download_url="https://github.com/arashyeganeh/tinypy/archive/v0.1.tar.gz",
    keywords=["file", "csv", "json", "md"],
    install_requires=["argparse"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={
        "Bug Reports": "https://github.com/arashyeganeh/tinypy/issues",
        "Source": "https://github.com/arashyeganeh/tinypy",
        "LinkedIn": "https://www.linkedin.com/in/arash-yeganeh",
    },
    python_requires=">=3.6",
)

if __name__ == "__main__":
    print("This is the wrong setup.py file to run")
