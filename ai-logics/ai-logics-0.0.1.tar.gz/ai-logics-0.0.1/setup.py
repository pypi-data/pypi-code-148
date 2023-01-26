from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Helpful in creating logics of any AI.'

# Setting up
setup(
    name="ai-logics",
    version=VERSION,
    author="Aditya Pratap Singh",
    author_email="pypi.aditya@outlook.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description='README.md',
    packages=find_packages(),
    install_requires=['pyttsx3', 'SpeechRecognition', 'wikipedia'],
    keywords=['logics', 'recogize', 'speech recognition', 'open apps', 'speak', 'ai', 'python ai', 'aditya pratap singh'],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: IBM Public License",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Python Software Foundation License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)