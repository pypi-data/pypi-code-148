from setuptools import setup, find_packages

setup(
    name='wayOfChange',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
    ],
    author='John Doe',
    author_email='johndoe@example.com',
    description='This is my awesome package',
    url='https://github.com/johndoe/mypackage',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)