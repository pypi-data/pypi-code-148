from setuptools import setup, find_packages


VERSION = '0.0.5'
DESCRIPTION = 'test file'
LONG_DESCRIPTION = 'A package that allows to test.'

# Setting up
setup(
    name="ThesisHNSC",
    version=VERSION,
    author="Akanksha",
    author_email="<akanksha20331@iiitd.ac.in>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['pandas','numpy','tensorflow','keras',],
    keywords=['python', 'Head and neck cancer', 'Diagnosis', 'Single cell', 'Genomics'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    include_package_data=True,
)
