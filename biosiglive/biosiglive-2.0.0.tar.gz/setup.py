from setuptools import find_packages, setup

setup(
    name="biosiglive",
    description="Biosignal processing and visualization in real-time.",
    version="2.0.0",
    author="Aceglia",
    author_email="amedeo.ceglia@umontreal.ca",
    # url="https://github.com/aceglia/biosiglive",
    license="MIT",
    packages=find_packages(include=["biosiglive", "biosiglive.*"]),
    keywords="biosiglive",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
