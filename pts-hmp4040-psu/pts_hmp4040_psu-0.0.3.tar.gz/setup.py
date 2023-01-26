from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pts_hmp4040_psu",
    version="0.0.3",
    author="Pass testing Solutions GmbH",
    description="Rohde & Schwarz HMP4040 PSU Diagnostic Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="shuparna@pass-testing.de",
    url="https://gitlab.com/pass-testing-solutions/fug-power-supply",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    py_modules=["pts_hmp4040_psu"],
    packages=find_packages(include=['pts_hmp4040_psu']),
    install_requires=["RsInstrument~=1.24.0.83", "pyvisa==1.12.0", "pyvisa-py==0.5.3", "aioredis~=1.3.1"],
    include_package_data=True,
)
