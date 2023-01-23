from setuptools import setup, find_packages

setup(
    name="TransformerModels",
    version="0.3.3",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["transformer_model_new_env"],
    },
    install_requires=['setfit','pandas'], 
    download_url='https://github.com/JoPulido123/TransformerModelDI/archive/refs/tags/0.3.3.tar.gz'
)
