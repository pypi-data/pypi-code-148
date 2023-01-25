from setuptools import setup, find_packages

setup(
    name='PyAR488',
    version='0.2.5',
    packages=find_packages(),
    url="https://github.com/Minu-IU3IRR/PyAR488",
    bugtrack_url = 'https://github.com/Minu-IU3IRR/PyAR488/issues',
    license='MIT',
    author='Manuel Minutello',
    description='module to interface AR488 boards and wide instrument library',
    long_description=open('README.md').read(),
    install_requires='pyserial',
    python_requeres = '>=3.6'
)