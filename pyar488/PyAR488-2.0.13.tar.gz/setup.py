from setuptools import setup, find_packages

verison_file = 'build_version.txt'

setup(
    name='PyAR488',
    version=open(verison_file).read(),
    packages=find_packages(exclude=("tests","build.py",'build_test.py','build_publish.py', 'build_version.txt', 'latest_version.txt', 'PyAR488.code-workspace')),
    url="https://github.com/Minu-IU3IRR/PyAR488",
    bugtrack_url = 'https://github.com/Minu-IU3IRR/PyAR488/issues',
    license='MIT',
    author='Manuel Minutello',
    description='module to interface AR488 boards and wide instrument library',
    long_description=open('README.md').read(),
    install_requires=('pyserial', 'numpy', 'matplotlib'),  # mathplotlib, numpy used for HP8903A
    python_requeres = '>=3.6'
)