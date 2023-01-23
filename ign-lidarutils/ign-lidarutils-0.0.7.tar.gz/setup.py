from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Lidar utils Python package'
LONG_DESCRIPTION = 'Common codes used in Lidar projects'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="ign-lidarutils",
    version=VERSION,
    author="Antoine Lavenant",
    author_email="<antoine.lavenant@ign.fr>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'lidar'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
