"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="innova-controls",
    version="2.0.2",
    description="Innova Air Conditioner Control API",
    license="Apache",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielrivard/innova-controls",
    author="Daniel Rivard",
    # author_email='author@example.com',  # Optional
    # https://pypi.org/classifiers/
    keywords="development, home automation, library, innova",
    packages=find_packages(exclude="test"),
    include_package_data=True,
    zip_safe=False,
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.9, <4",
    install_requires=["aiohttp >= 3.0.0, < 4.0.0","retry2>=0.9.3"],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/danielrivard/innova-controls/issues",
        "Source": "https://github.com/danielrivard/innova-controls/",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)
