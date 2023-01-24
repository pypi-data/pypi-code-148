import setuptools

with open(r"README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LonginusAlpha",
    version="0.4.7",
    author="Example Author",
    author_email="team.longinus.project@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/projectlonginus/LonginusPYPI",
    install_requires=['pyCryptodome','asyncio','argon2-cffi','requests'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.11',
)