from setuptools import setup, find_packages

with open("README.md") as file:
    long_description = file.read()

with open("requirements.txt") as file:
    install_requires = file.read().strip().split("\n")

setup(
    name="robin_sd_upload",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
    'console_scripts': [
        'robin-sd-upload = robin_sd_upload.__main__:main',
    ],
    },
    version="0.1.46",
    license="MIT",
    description="Package to upload files to the Robin Radar API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Robin Radar Systems",
    author_email="tivadar.kamondy@robinradar.com",
    url="https://bitbucket.org/robin-radar-systems/sd-api-upload-pip-package.git",
    keywords=["python", "robin", "radar", "download", "software", "sd"]
)
