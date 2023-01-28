from setuptools import setup, find_packages


VERSION = '0.0.1'


# Setting up
setup(
    name="trainers_cooks",
    version=VERSION,
    packages=find_packages(),
    install_requires=['requests', 'pycrypto'],
    keywords=['python', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)