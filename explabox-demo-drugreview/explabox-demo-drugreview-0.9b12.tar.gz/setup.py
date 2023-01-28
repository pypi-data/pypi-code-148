import setuptools
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(  # type: ignore
    name="explabox-demo-drugreview",
    version="0.9b12",
    description="Explabox demo for the UCI drug reviews dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="NPAI",
    packages=setuptools.find_packages(),  # type : ignore
    install_requires=["explabox>=0.9b7", "jupyter>=1.0.0", "tokenizers>=0.11.6", "transformers", "tqdm>=4.62.3"],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={"": ["assets/drugsCom.zip", "assets/tokenizer.pkl"]}
)
