from setuptools import setup, find_packages

setup(
        # the name must match the folder name 'verysimplemodule'
        name="Belrub 2.2.1", 
        version='2.2.1',
        author="Mamad Belectron",
        author_email="",
        description='This is a Library for robots in Rubika',
        long_description='## How To Import\n from Belrub import Token',
        packages=find_packages(),
        
        # add any additional packages that 
        # needs to be installed along with your package.
        install_requires=["pycryptodome==3.16.0", "Pillow==9.4.0"], 
        
        keywords=['python', 'rubika', 'Belrub', 'rubel', 'Rubika', 'belectron', 'robika', 'robot'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
        ]
)
