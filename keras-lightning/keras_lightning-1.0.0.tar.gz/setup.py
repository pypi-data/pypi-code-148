import setuptools

setuptools.setup(
    name='keras_lightning',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    version="1.0.0",
    author="Alan T. L. Bacellar",
    author_email="alanbacellar@gmail.com",
    description="Minimal Keras like wrapper for torch-lightning",
    url="https://github.com/Alantlb/keras_lightning",
    install_requires=[
        'torch',
        'pytorch-lightning',
        'torchmetrics'
    ]
)