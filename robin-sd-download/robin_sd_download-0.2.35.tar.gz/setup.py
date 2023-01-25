from setuptools import setup

with open("README.md") as file:
    long_description = file.read()

setup(
    name="robin_sd_download",
    packages=["robin_sd_download"],
    install_requires=["validators>=0.18.2", "PyYAML>=5.4.1", "requests>=2.25.1"],
    entry_points={
    'console_scripts': [
        'robin_sd_download = robin_sd_download.__main__:main',
    ],
    },
    version="0.2.35",
    license="MIT",
    description="Package to download files to the Robin Radar API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Robin Radar Systems",
    author_email="tivadar.kamondy@robinradar.com",
    url="https://bitbucket.org/robin-radar-systems/sd-api-download-pip-package.git",
    keywords=["python", "robin", "radar", "download", "software", "sd"]
)
