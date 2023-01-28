from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'A basic Atto-Host API'
LONG_DESCRIPTION = 'A basic API for sending files to and receiving files form Atto-Host web storage server'

# Setting up
setup(
    name="atto-api",
    version=VERSION,
    author="ewbrowntech (Ethan Brown)",
    author_email="<ewbrowntech@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'file management', 'API'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)