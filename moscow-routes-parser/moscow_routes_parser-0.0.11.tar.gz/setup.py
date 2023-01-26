import setuptools
from setuptools import setup

setup(
    name='moscow_routes_parser',
    version='0.0.11',
    url='https://github.com/rscprof/moscow_routes_parser',
    license='MIT',
    author='rscprof',
    author_email='rscprof@gmail.com',
    description='Parser for t.mos.ru to get routes and timetables of buses, tramways and trolleybus',
#    package_dir={"": "src"},
    packages=setuptools.find_packages(where="moscow_source_parser"),
    requires=['requests']
)
