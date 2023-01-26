import setuptools
from setuptools import setup

setup(
    name='moscow_routes_parser',
    version='0.0.19',
    url='https://github.com/rscprof/moscow_routes_parser',
    license='MIT',
    author='rscprof',
    author_email='rscprof@gmail.com',
    description='Parser for t.mos.ru to get routes and timetables of buses, tramways and trolleybus',
    packages=["moscow_routes_parser"],
    requires=['requests']
)
