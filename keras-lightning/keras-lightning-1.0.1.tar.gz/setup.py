import setuptools

setuptools.setup(
    name='keras-lightning',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    version="1.0.1",
    author="Alan T. L. Bacellar",
    author_email="alanbacellar@gmail.com",
    description="Minimal Keras like wrapper for torch-lightning",
    url="https://github.com/Alantlb/keras-lightning",
    install_requires=[
        'torch',
        'pytorch-lightning',
        'torchmetrics'
    ]
)