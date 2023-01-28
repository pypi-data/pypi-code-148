from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'NASTRAN BDF Reader'
LONG_DESCRIPTION = 'NASTRAN BDF file reader'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="nastran_reader", 
        version=VERSION,
        author="Domhnall Morrissey",
        author_email="<domhnallmorr@yahoo.co.uk>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        py_modules = ["nastran_reader"],
        keywords=['python', 'nastran'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)