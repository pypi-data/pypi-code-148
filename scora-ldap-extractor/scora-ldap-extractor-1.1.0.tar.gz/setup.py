from setuptools import setup, find_packages
from pkgver import package_version
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


install_reqs = [
    "ldap3>=2.9.1",
    "boto3>=1.26.57",
    "python-dotenv>=0.21.1",
    "environs>=9.5.0",
    "numpy>=1.24.1",
]

setup(
    name="scora-ldap-extractor",
    packages=find_packages(exclude=["*.env"]),
    package_dir={"scora_ldap_extractor": "src"},
    version=package_version,
    description="Scora Ldap Extractor, see docs for more details.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=True,
    install_requires=install_reqs,
    python_requires=">=3.8",
    author="Oncase",
    author_email="contato@oncase.com.br",
    url="https://github.com/oncase/scora-ldap-extractor",
    license="MIT",
    keywords="scora",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
    ],
)
