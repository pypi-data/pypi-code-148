from setuptools import setup, find_packages

with open("README.md", "r") as fh:

    long_description = fh.read()


setup(
    name='prettify_py',
    version='0.2.3.1',
    packages=find_packages(include=["prettify_py"]),
    include_package_data=True,
    install_requires=[
        'Click',
        'docformatter', 
        'black', 
        "amarium"
    ],
    entry_points={
        'console_scripts': [
            'prettify-py = prettify_py.formatter:format_py',
        ],
    },
    author="Julian M. Kleber",
    author_email="julian.kleber@sail.black",
    description="CLI for prettifying XML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.codeberg/cap_jmk/prettify-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
