from setuptools import setup
import os

VERSION_PATH = os.path.join("ai_metadata", "version.py")
exec(open(VERSION_PATH).read())

VERSION = __version__ # noqa

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ai-metadata",
    version=VERSION,
    description="Detect and extract metadata about AI/ML models for deployment and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["ai_metadata"],
    # include_package_data=True,
    install_requires=[
        "numpy", "pandas", "scikit-learn", "pypmml", "onnxruntime"
    ],
    tests_require=["pytest"],
    url="https://github.com/autodeployai/ai-metadata",
    download_url="https://github.com/autodeployai/ai-metadata/archive/v" + VERSION + ".tar.gz",
    author="AutoDeployAI",
    author_email="autodeploy.ai@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
)

