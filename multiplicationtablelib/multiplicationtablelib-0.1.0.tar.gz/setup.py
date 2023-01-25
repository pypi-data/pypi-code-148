from setuptools import find_packages, setup
setup(
    name='multiplicationtablelib',
    packages=find_packages(include=['multiplicationtablelib']),
    version='0.1.0',
    description='Python library for showing multiplication tables',
    long_description_content_type='text/markdown',
    long_description='README',
    author='Sarthak, Arpit',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)