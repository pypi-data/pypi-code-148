from setuptools import find_packages, setup

setup(
    name='manosutils',
    packages=find_packages(include=['manosutils']),
    version='0.1.0',
    description="Things I'm tired of writing manually in a library!",
    author='Manos Wagner',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.2.1'],
    test_suite='tests',
)