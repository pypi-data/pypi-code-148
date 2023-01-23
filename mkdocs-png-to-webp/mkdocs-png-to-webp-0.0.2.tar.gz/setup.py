from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pip>=22", "mkdocs>=1", "webptools==0.0.9"]

entry_points={
    'mkdocs.plugins': [
        'mkdocs-png-to-webp = mkdocs-png-to-webp:ConvertPngToWebp',
    ]
}

setup(
    name="mkdocs-png-to-webp",
    version="0.0.2",
    author="mur4d1n",
    author_email="mur4d1n@yandex.ru",
    description="A package to convert your mkdocs images from png to webp",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mur4d1n-lib/mkdocs-png-to-webp/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
