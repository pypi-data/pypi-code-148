from setuptools import setup, find_packages
from pkgver import package_version


install_reqs = [
    "ldap3>=2.9.1",
    "boto3>=1.26.57",
    "python-dotenv>=0.21.1",
    "environs>=9.5.0",
]

setup(
    name="scora-ldap-extractor",
    packages=find_packages(include=["src", "pkgver"]),
    version=package_version,
    description="Scora Ldap Extractor, see docs for more details.",
    zip_safe=True,
    install_requires=install_reqs,
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
