from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="Audio-Quality-Scorer",
    version="1.0",
    author="Dr Dheiver Francisco Santos",
    author_email="dheiver.santos@gmail.com",
    description="A library for scoring audio quality using SNR, THD, and CR metrics.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dheiver-Santos87/AudioQualityScorer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    install_requires=[
        "scipy",
        "numpy",
        "pandas",
        "matplotlib",
        "csv"
    ],
)
