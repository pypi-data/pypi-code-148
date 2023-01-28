import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pipeforce-sdk-python",                     # This is the name of the package
    version="9.0.0",                        # The initial release version
    author="LOGABIT GmbH",                     # Full name of the author
    description="Python SDK for PIPEFORCE",
    long_description=long_description,      # Long description read from the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.9',                # Minimum version requirement of the package
    py_modules=["pipeforce"],             # Name of the python package
    package_dir={'':'pipeforce-sdk-python/src'},     # Directory of the source code of the package
    install_requires=[]                     # Install other dependencies if any
)