from setuptools import setup, find_packages
import pathlib
import dnn_cool_losses

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="dnn_cool_losses",
    version=dnn_cool_losses.__version__,
    description="dnn_cool_losses: Per-sample loss functions and utilities",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hristo-vrigazov/dnn_cool_losses",
    author="Hristo Vrigazov",
    author_email="hvrigazov@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["numpy", "dnn_cool_activations"],
)
