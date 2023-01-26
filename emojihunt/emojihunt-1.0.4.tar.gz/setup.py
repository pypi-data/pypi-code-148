import setuptools

setuptools.setup(
    name="emojihunt",                     # This is the name of the package
    version="1.0.4",                        # The initial release version
    author="Declan McIntosh",                     # Full name of the author
    description="UVIC ECE471 Project Code for 2023",
    long_description="UVIC ECE471 Project Code for 2023",      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["emojihunt","emojihunt.emojihunt","emojihunt.templates"],             # Name of the python package
    package_dir={'':'emojihunt/'},     # Directory of the source code of the package
    install_requires=[  'keras>=2.8.0',
                        'imgaug==0.4.0',
                        'opencv-python>=4.1.2.30',
                        'Pillow'],                     # Install other dependencies if any
    include_package_data=True,
    package_data={'emojihunt': ['NONE']}
)