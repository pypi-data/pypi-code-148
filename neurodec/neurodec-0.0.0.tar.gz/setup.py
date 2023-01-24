from setuptools import setup

setup(
    name='neurodec',
    version='0.0.0',
    packages=['neurodec'],
    license='',
    author='neurodec',
    description='A Python package that provides access to all of the neurodec software tools.',
    scripts=['scripts/neurodec'],
    install_requires=[
        'werkzeug',
        'trimesh',
        'numpy',
    ],
)
