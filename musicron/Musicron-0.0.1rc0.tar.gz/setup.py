from setuptools import setup,find_packages

setup(
    name="Musicron",
    version="0.0.1RC",
    author="Wesley Fisher",
    author_email="wfisher@praetor.tel",
    description="A cron for music!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gwfisher/musicron",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "pyyaml",
        "dbus-python",
        "pathlib",
        "importlib",
        "psutil",
        "python-dateutil"
    ],
)
